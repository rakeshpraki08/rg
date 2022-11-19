from celery import shared_task

import psycopg2
import pandas as pd
import os
import cx_Oracle
import time, math, ast

import json

from datetime import datetime 

from .models import CustomUser, Regions, Reports, Reports_Data

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

# from django.contrib import messages

@shared_task(bind = True)
def data_fetch(self, id):
    try:
        
        print("id", id)
        report_data = Reports.objects.filter(id=id).values()
        report_data.update(Task_Status = "Running") 
        print("running updated ", report_data[0]['Task_Status'])
        
        msg = {
            "status":report_data[0]['Report_Name']+" job started",
            "btn":False,
            "id":id,
               }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'fetch_data',
            {
                'type': 'task_message',
                'message': msg,
            }
        )
        # print("report_data", report_data)
        # print("sql data", report_data[0]['Sql_Query'])
        # print("Region_id", report_data[0]['Region_id'])
        region_data = Regions.objects.filter(Region=report_data[0]['Region_id']).values()
        print("region_data", region_data[0]['Region'])
        
        start_time = time.time()
        print('start_time', start_time)
        con_str = {
            'DB_HOST' : region_data[0]['DB_Host'],
            'PORT' : region_data[0]['DB_Port'],  
            'DB_USER' : 'base_sip',
            'DB_PASS' : 'Ifg5p_gPlm632',
            'service' : region_data[0]['DB_Service_Name'],    
        }
        
        conn = cx_Oracle.connect('{DB_USER}/{DB_PASS}@{DB_HOST}:{PORT}/{service}'.format(**con_str))
        
        print("connection established")
        
        msg = {
            "status":report_data[0]['Report_Name']+" job connection established",
            "btn":False,
            "id":id,
               }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'fetch_data',
            {
                'type': 'task_message',
                'message': msg,
            }
        )
        
        sqlquery = report_data[0]['Sql_Query']
        df = pd.read_sql(sql = sqlquery, con = conn)
        print(type(df))
        # print(df)
        print("len of data fetched", len(df))
        print("data fetched")
        
        report_query = Reports_Data.objects.filter(Report_Name = report_data[0]['Report_Name']).values()
        if report_query:
            print("updating Reports_Data")
            report_query.update(Data_Fetched = df.to_json())
            # report_query.update(Last_Run = datetime.now())
        else:
            print("creating Reports_Data")
            r_Name = report_data[0]['Report_Name']
            Reports_Data.objects.create(Report_Name = r_Name, 
                                        Data_Fetched = df.to_json())    
        
        report_data.update(Last_Run = datetime.now())
        print("date updated", report_data[0]['Last_Run'])
        report_data.update(Task_Status = "Completed")
        print("completed updated", report_data[0]['Task_Status'])
        # data_to_update = Reports.objects.filter(id=id)
        # print("data inserted ", updated_data)
        # print("updated data ", report_data[0]['Data_Fetched'])
        # print("Data fetch completed for region ", region_data[0]['Region'])
        
        msg = {
            "status":report_data[0]['Report_Name']+" job completed",
            "btn":True,
            "id":id,
               }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'fetch_data',
            {
                'type': 'task_message',
                'message': msg,
            }
        )
        
        # time.sleep(5)

        # msg = {
        #     "status":"",
        #     "btn":"completed",
        #     "id":id,
        #        }
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        # 'fetch_data',
        #     {
        #         'type': 'task_message',
        #         'message': msg,
                
        #     }
        # )
        
        return 'Done'

        
    except Exception as error:
        print("thread error ", [type(error), error])
        # error_json = json.dumps({'error' : error.DatabaseError.cx_Oracle._Err()})
        # print("thread error json ", [type(error_json), error_json])
        error_string = str(error)
        msg = {
            "status":error_string,
            "btn":"error",
            "id":id,
               }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'fetch_data',
            {
                'type': 'task_message',
                'message': msg,
                
            }
        )
        print("thread error string ", [type(error_string), error_string])
        return error_string
        # messages.error(request, error)
        
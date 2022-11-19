from django.urls import path
from query_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "query_app"
urlpatterns = [
    
    
    # ------------ e-mail ----------
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),
    
    # -------login----------
    
    path('',views.loginPage, name = 'login-page' ),
    path('login/<str:s>/',views.loginPage_Revert, name = 'login-page-revert' ),
    path('logout/',views.logoutPage, name = 'logout-page' ),
    path('register/',views.registerPage, name = 'register-page' ),
    
    # path('extract/<int:id>/', views.extract, name = 'extract'),
    # path('Reports/<str:region>/', views.home, name = 'home'),
    
    # ----- admin -----
    
    # path('RGadmin/', views.base_html_Admin, name = 'base_html_Admin'),
    
    # ----- normal users ------  
    
      
    path('extract/<int:id>/', views.extract, name = 'extract'),
    path('fetch_data/<int:id>/', views.fetch_data, name = 'fetch_data'),
    
    
    path('Reports/<str:region>/', views.base_html_region, name = 'base_html_region'),
    path('AjaxReports/<int:id>/', views.get_Ajax_LastRun, name = 'get_Ajax_LastRun'),
    # path('AjaxReports/', views.get_Ajax_LastRun, name = 'get_Ajax_LastRun'),
   
    path('home/', views.base_html, name = 'base_html'),
    
    # path('user/', views.base_html_User, name = 'base_html_User'),
    
    # -----------------Reports---------------------
    
    # path('insert_report/', views.insert_report, name = 'insert_report'),
    path('manage_reports/', views.list_reports, name = 'manage_reports'),
    path('delete_report/<int:id>/', views.delete_report, name='delete_report'),
    path('manage_reports/<int:id>/', views.list_reports, name = 'manage_reports_update'),
    
    # -------------------Regions---------------------
    
    path('manage_regions/', views.list_regions, name = 'manage_regions'),
    path('delete_region/<str:region>/', views.delete_region, name='delete_region'),
    path('manage_regions/<str:region>/', views.list_regions, name = 'manage_regions_update'),
    
    
    # --------------------Users-----------------------
    
    path('manage_users/', views.list_users, name = 'manage_users'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('manage_users/<int:id>/', views.list_users, name = 'manage_users_update'),
    path('pending_user_request/', views.pending_user_request, name = 'pending_user_request'),
    path('accept_user_request/<int:id>', views.accept_user_request, name = 'accept_user_request'),
    path('reject_user_request/<int:id>', views.reject_user_request, name = 'reject_user_request'),
    # path('user_region_request_edit/', views.user_region_request_edit, name = 'user_region_request_edit'),
]

urlpatterns += staticfiles_urlpatterns()
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from django.forms import HiddenInput
from .models import Regions, Reports

from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["email"].widget.attrs.update({
            # 'class' : 'form-input',
            'type' : 'text',
            'name' : 'E-mail',
            # 'placeholder' : 'E-mail',
        })
        
        self.fields["password1"].widget.attrs.update({
            # 'class' : 'form-input',
            'type' : 'password',
            'name' : 'password1',
            # 'placeholder' : 'Password',
        })
        
        self.fields["password2"].widget.attrs.update({
            # 'class' : 'form-input',
            'type' : 'password',
            'name' : 'password2',
            # 'placeholder' : 'Re-Password',
        })
        
        self.fields["regions"].widget.attrs.update({
           
           
        })
        
        self.fields["is_staff"].widget.attrs.update({
           
            
        })
        
        self.fields["is_active"].widget.attrs.update({
           
            
        })
                
        self.fields["is_superuser"].widget.attrs.update({
           
           
        })
        
    regions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Regions.objects.all())    

    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active', 'is_superuser','password1', 'password2', 'regions')
        


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["email"].widget.attrs.update({
           
            # 'type' : 'text',
            # 'name' : 'E-mail',
            # 'placeholder' : 'E-mail',
        })
        
        self.fields["password"].widget.attrs.update({
           
            # 'type' : 'password',
            # 'name' : 'password',
            # 'placeholder' : 'Password',
        })
        
        # self.fields["password2"].widget.attrs.update({
      
        #     'type' : 'password',
        #     'name' : 'password2',
        #     'placeholder' : 'Re-Password',
        # })
        
        self.fields["is_staff"].widget.attrs.update({
            
            
          
            # 'type' : 'checkbox',
            # 'name' : 'is_staff',
        })
        
        self.fields["is_active"].widget.attrs.update({
            
           
            # 'type' : 'checkbox',
            # 'name' : 'is_active',
        })
                
        self.fields["is_superuser"].widget.attrs.update({
        
           
            
            # 'type' : 'checkbox',
            # 'name' : 'is_superuser',
        })
        
        self.fields["regions"].widget.attrs.update({
            # 'class' : 'check-box-field',
            # 'type' : 'password',
            # 'name' : 'password1',
            # 'placeholder' : 'Password',
        })
        
    regions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Regions.objects.all())
    
    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active','is_superuser', 'password', 'regions')
        
# ----------for registration ---------
class CustomRegisterCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        self.fields["email"].widget.attrs.update({
            # 'class' : 'input100',
            'id' : 'email-registration',
            'type' : 'text',
            'name' : 'E-mail',
            # 'placeholder' : 'E-mail',
        })
        
        self.fields["password1"].widget.attrs.update({
            # 'class' : 'input100',
            'type' : 'password',
            'name' : 'password1',
            # 'placeholder' : 'Password',
        })
        
        self.fields["regions"].widget.attrs.update({
            # 'class' : 'check-box-field',
            # 'type' : 'password',
            # 'name' : 'password1',
            # 'placeholder' : 'Password',
        })
        
        self.fields["password2"].widget.attrs.update({
            # 'class' : 'input100',
            #  'type' : 'password',
            # 'name' : 'password2',
            # 'placeholder' : 'Re-Password',
        })
        
        self.fields["is_staff"].widget.attrs.update({
            # 'class' : 'check-box-field',
            # 'id' : "ckb1",
            # 'type' : 'checkbox',
            # 'name' : 'is_staff',
            # 'label' : 'is_staff',
        })
        
    regions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Regions.objects.all())
    
    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active','password1', 'password2', 'regions')




# --------------------------------
        
        
# ----- for admin page -----------
class CustomAdminCreationForm(UserCreationForm):
    
    # regions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Regions.objects.all())
    
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomAdminChangeForm(UserChangeForm):
    

    class Meta:
        model = CustomUser
        fields = ('email',)

# -------------------------------------
        
class ReportsForm(forms.ModelForm):
    
    # Report_Name = forms.CharField(widget=forms.TextInput(attrs = {"class" : "form-control",
    #             "id" : "dbHost", 
    #             "name" : "db_host",
    #             "type" : "text",
    #             "placeholder" : "DB_Host",
    #             "data-sb-validations" : "required",
    #         }))
    # Sql_Query = forms.CharField(widget=forms.TextInput(attrs = {"class" : "form-control",
    #             "id" : "dbHost", 
    #             "name" : "db_host",
    #             "type" : "text",
    #             "placeholder" : "DB_Host",
    #             "data-sb-validations" : "required",
    #         }))
    # Region = forms.InlineForeignKeyField(widget=forms.TextInput(attrs = {"class" : "form-control",
    #             "id" : "dbHost", 
    #             "name" : "db_host",
    #             "type" : "text",
    #             "placeholder" : "DB_Host",
    #             "data-sb-validations" : "required",
    #         })
    
    class Meta:
        model = Reports
        fields = ['Report_Name', 'Sql_Query', 'Region']
        
        widgets = {
            'Report_Name' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "dbHost", 
                # "name" : "db_host",
                # "type" : "text",
                # # "placeholder" : "DB_Host",
                # "data-sb-validations" : "required",
            }),
            
            'Sql_Query' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "dbHost", 
                # "name" : "db_host",
                # "type" : "text",
                # # "placeholder" : "DB_Host",
                # "data-sb-validations" : "required",
            }),

            'Region' : forms.Select(attrs = {
                # "class" : "form-control",
                # "id" : "dbHost", 
                # "name" : "db_host",
                # "type" : "text",
                # # "placeholder" : "DB_Host",
                # "data-sb-validations" : "required",
                'style' : """ border-radius: 5px;
                cursor: pointer;
                margin-bottom: 30px;
                font-size: 12px;
                font-family: sans-serif; """,
                
            }),
        }
    
    def __init__(self,*args, **kwargs):
        super(ReportsForm, self).__init__(*args, **kwargs)
        self.fields['Region'].empty_label = "Select"
        
        
class RegionsForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ['Region', 'DB_Host', 'DB_Service_Name', 'DB_Port']
        
        widgets = {
            'Region' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "region", 
                # "name" : "region",
                # "type" : "text",
                # "placeholder" : "Region",
                # "data-sb-validations" : "required",
            }),
            
            'DB_Host' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "dbHost", 
                # "name" : "db_host",
                # "type" : "text",
                # "placeholder" : "DB_Host",
                # "data-sb-validations" : "required",
            }),

            'DB_Service_Name' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "dbservicename", 
                # "name" : "db_service_name",
                # "type" : "text",
                # "placeholder" : "DB_Service_Name",
                # "data-sb-validations" : "required",
            }),
            
            'DB_Port' : forms.TextInput(attrs = {
                # "class" : "form-control",
                # "id" : "dbport", 
                # "name" : "db_port",
                # "type" : "text",
                # "placeholder" : "DB_Port",
                # "data-sb-validations" : "required",
            }),
        }
from django import forms
from UserApp.models import *



# Choices for country codes
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentUploadsModel
        fields = [
            'student',
            'countrycode',
            'whatsapp_number',
            'university',
            'course',
            'module_name',
            'total_word_count',
            'submission_date',
            'expected_delivery_date',
            'assignment_file',
            'model_work',
            'module_materials',
            'instructions',
            'country_specific',
            'country_specific_name',
            'company_specific',
            'company_specific_name'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select form-control'}),
            'countrycode': forms.Select( attrs={'class': 'form-select form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Whatsapp Number'}),
            'university': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'University'}),
            'course': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Course'}),
            'module_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Module Name'}),
            'total_word_count': forms.NumberInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Word Count'}),
            'submission_date': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'assignment_file': forms.FileInput(attrs={'class': 'form-file'}),
            'model_work': forms.FileInput(attrs={'class': 'form-file'}),
            'module_materials': forms.FileInput(attrs={'class': 'form-file'}),
            'instructions': forms.FileInput(attrs={'class': 'form-file'}),
            'country_specific_name': forms.TextInput(
                attrs={'placeholder': 'Enter Country Specific Name', 'class': 'form-control form-control-user'}),
            'company_specific_name': forms.TextInput(
                attrs={'placeholder': 'Enter Company Specific Name', 'class': 'form-control form-control-user'}),
        }

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = UsersModel.objects.filter(user_type__user_type='Student')


class UserForm(forms.ModelForm):
    class Meta:
        model = UsersModel
        fields = ['first_name', 'last_name', 'mailid', 'password', 'user_type']
        widgets ={
            'first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
            'mailid': forms.EmailInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}),
            'user_type': forms.Select(attrs={'class': 'form-select form-control'})
        }

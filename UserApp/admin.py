from django.contrib import admin
from UserApp.models import *

# Register your models here.

admin.site.register(UserType)

admin.site.register(FacultyAssignModel)
admin.site.register(FacultyAnswerModel)



admin.site.register(UsersModel)
admin.site.register(StudentUploadsModel)
admin.site.register(CountryCodeModel)
admin.site.register(PlagiarismModel)
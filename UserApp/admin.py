from django.contrib import admin
from UserApp.models import *

# Register your models here.

admin.site.register(StudentFileModel)
admin.site.register(UserType)
admin.site.register(UserModel)
admin.site.register(FacultyAssignModel)
admin.site.register(FacultyAnswerModel)
admin.site.register(ManagerErrorFileModel)
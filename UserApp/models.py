from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.
class UserType(models.Model):
    usertype_id = models.AutoField(primary_key = True)
    user_type = models.CharField(
        max_length=20,

    )
    def __str__(self):
        return self.user_type

class UserModel(models.Model):
    user_id = models.CharField(primary_key=True, max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mailid = models.EmailField()
    password = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(pre_save, sender=UserModel)
def generate_unique_id(sender, instance, **kwargs):
    if not instance.user_id:
        last_admin = UserModel.objects.all().order_by('user_id').last()
        if last_admin and last_admin.user_id.startswith('USR'):
            try:
                new_id = int(last_admin.user_id.split('USR')[-1]) + 1
            except ValueError:
                new_id = 1
        else:
            new_id = 1
        instance.user_id = f"USR{new_id:05d}"

class UsersModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mailid = models.EmailField()
    password = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentFileModel(models.Model):
    studentfile_id = models.AutoField(primary_key = True)
    student = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    country_code = models.CharField(max_length=5)  # For country code like +1, +91, etc.
    whatsapp_number = models.CharField(max_length=15)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    total_word_count = models.IntegerField()
    submission_date = models.DateField()
    expected_delivery_date = models.DateField()
    assignment_file = models.FileField(upload_to='assignments/')
    uploaded_date = models.DateField()

    country_specific = models.BooleanField(default=False)
    country_specific_name = models.CharField(max_length=100, blank=True, null=True)
    company_specific = models.BooleanField(default=False)
    company_specific_name = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.student.user_type.user_type != 'Student':
            raise ValidationError("The selected user is not a student.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean method to ensure validation is applied during save
        super(StudentFileModel, self).save(*args, **kwargs)



class CountryCodeModel(models.Model):
    country_id = models.AutoField(primary_key = True)
    country_code = models.CharField(max_length = 50)
    country_name = models.CharField(max_length = 100)

    def __str__(self):
        return f"({self.country_code}) {self.country_name}"


class StudentUploadsModel(models.Model):
    studentfile_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(UsersModel, on_delete=models.CASCADE, null=True)

    countrycode = models.ForeignKey(CountryCodeModel, on_delete = models.CASCADE, null = True)
    whatsapp_number = models.CharField(max_length=15)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    total_word_count = models.IntegerField()
    submission_date = models.DateField()
    expected_delivery_date = models.DateField()
    assignment_file = models.FileField(upload_to='assignments/')
    model_work = models.FileField(upload_to = 'model-work/', null=True, blank=True)
    module_materials = models.FileField(upload_to = 'module_materials/', null=True, blank=True)
    instructions = models.FileField(upload_to = 'instructions/', null=True, blank=True)
    uploaded_date = models.DateField()

    country_specific = models.BooleanField(default=False)
    country_specific_name = models.CharField(max_length=100, blank=True, null=True)
    company_specific = models.BooleanField(default=False)
    company_specific_name = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.student.user_type.user_type != 'Student':
            raise ValidationError("The selected user is not a student.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean method to ensure validation is applied during save
        super(StudentUploadsModel, self).save(*args, **kwargs)



class FacultyAssignModel(models.Model):
    assign_id = models.AutoField(primary_key = True)
    assigned_by = models.ForeignKey(UsersModel, on_delete=models.CASCADE, null=True, related_name='Manager')
    assigned_to = models.ForeignKey(UsersModel, on_delete=models.CASCADE, null=True, related_name='Faculty')
    file = models.ForeignKey(StudentUploadsModel, on_delete=models.CASCADE)
    assigned_time = models.DateTimeField()


class FacultyAnswerModel(models.Model):
    Verifying = 'Verifying'
    Error = 'Error'
    Completed = 'Completed'
    STATUS_CHOICES = [
        (Verifying, 'Verifying'),
        (Error, 'Error'),
        (Completed, 'Completed'),
    ]
    answer_id = models.AutoField(primary_key=True)
    faculty = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    assigned_file = models.OneToOneField(FacultyAssignModel, on_delete=models.CASCADE)
    answer_file = models.FileField(upload_to='faculty_answers/')
    uploaded_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=Verifying
    )

    def __str__(self):
        return f"Answer by {self.faculty.first_name} for {self.assigned_file.file.assignment_file}"


class PlagiarismModel(models.Model):
    error_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    faculty_answer = models.OneToOneField(FacultyAnswerModel, on_delete=models.CASCADE)
    plagiarism_report = models.FileField(upload_to='manager_errors/', null=True, blank=True)
    ai_report = models.FileField(upload_to = 'plagiarism_report/', null=True, blank=True)
    proof_reading = models.FileField(upload_to = 'proof_reading/', null=True, blank=True)
    uploaded_date = models.DateTimeField()

    def __str__(self):
        return f"Error by {self.manager.first_name} for {self.faculty_answer.assigned_file.file.assignment_file}"


# New model for Manager's error files
class ManagerErrorFileModel(models.Model):
    error_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    faculty_answer = models.OneToOneField(FacultyAnswerModel, on_delete=models.CASCADE)
    error_file = models.FileField(upload_to='manager_errors/', null=True, blank=True)
    uploaded_date = models.DateTimeField()

    def __str__(self):
        return f"Error by {self.manager.first_name} for {self.faculty_answer.assigned_file.file.assignment_file}"


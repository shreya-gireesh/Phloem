from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from UserApp.forms import *
from UserApp.models import *


# Create your views here.
def student_home(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"
        response_data = []

        # Querying for files uploaded by the logged-in student
        uploaded_files = StudentFileModel.objects.filter(student=loggedin_user)
        for student_file in uploaded_files:
            student_name = f"{student_file.student.first_name} {student_file.student.last_name}"
            # Get the assignment details (Faculty who is assigned)
            faculty_assignment = FacultyAssignModel.objects.filter(file=student_file).first()

            if faculty_assignment:
                assigned_faculty = faculty_assignment.assigned_to
                faculty_name = f"{assigned_faculty.first_name} {assigned_faculty.last_name}"

                # Get the faculty answer (if any)
                faculty_answer = FacultyAnswerModel.objects.filter(assigned_file=faculty_assignment).first()
                answer_file_url = faculty_answer.answer_file.url if faculty_answer else None

                data = {
                    "student_name": student_name,
                    "student_file": student_file.assignment_file.url,
                    "delivery_date": student_file.expected_delivery_date,
                    "faculty_assigned": faculty_name,
                    "faculty_answer_file": answer_file_url
                }
            else:
                data = {
                    "student_name": student_name,
                    "student_file": student_file.assignment_file.url,
                    "delivery_date": student_file.expected_delivery_date,
                    "faculty_assigned": None,
                    "faculty_answer_file": None
                }

            response_data.append(data)

        return render(request, 'index.html', {'username': username, 'uploaded_files': response_data})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        try:
            user = UserModel.objects.get(mailid=email, password=password, user_type__user_type = user_type)
            request.session['user'] = user.user_id
            request.session['user-type'] = user.user_id
            request.session.set_expiry(3600)
            if user.user_type.user_type == 'Student':
                return redirect('/')
            elif user.user_type.user_type == 'Teacher':
                return redirect('/faculty')
            elif user.user_type.user_type == 'Manager':
                return redirect('/manager')
        except UserModel.DoesNotExist:
            return render(request, 'login.html', {'error': "User not found"})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def submissionform(request):
    today = datetime.now().date()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission_form = form.save(commit=False)
            submission_form.uploaded_date = today  # Set the admin field from the logged-in user
            submission_form.save()
            return redirect('/')  # Redirect to a relevant page after submission
    else:
        form = SubmissionForm()

    return render(request, 'submission-form.html', {'form': form})


def manager(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"
        # Fetch only unassigned student files (i.e., those that are not present in FacultyAssignModel)
        assigned_files = FacultyAssignModel.objects.values_list('file_id', flat=True)
        student_files = StudentFileModel.objects.exclude(studentfile_id__in=assigned_files)

        # Fetch all teachers
        teachers = UserModel.objects.filter(user_type__user_type='Teacher')

        if request.method == 'POST':
            file_id = request.POST.get('file_id')
            teacher_id = request.POST.get('teacher_id')

            if file_id and teacher_id:
                file = StudentFileModel.objects.get(studentfile_id=file_id)
                teacher = UserModel.objects.get(user_id=teacher_id)

                # Fetch the corresponding UserModel instance for the logged-in manager
                manager = UserModel.objects.get(user_id=user)

                # Create a new FacultyAssignModel entry
                FacultyAssignModel.objects.create(
                    assigned_by=manager,
                    assigned_to=teacher,
                    file=file,
                    assigned_time=datetime.now()
                )

                return redirect('/manager')
    return render(request, 'manager.html', {'username': username, 'student_files': student_files, 'teachers': teachers, 'user_type': loggedin_user.user_type.user_type})

def faculty_home(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"
        today = datetime.now().date()

        # Get all the assignments
        assignments = FacultyAssignModel.objects.filter(assigned_to=loggedin_user, file__expected_delivery_date = today)

        # Prepare the response data
        response_data = []

        for assignment in assignments:
            student_file = assignment.file
            student_name = f"{student_file.student.first_name} {student_file.student.last_name}"
            delivery_date = assignment.file.expected_delivery_date
            faculty_answer = FacultyAnswerModel.objects.filter(assigned_file=assignment).first()
            manager_error = ManagerErrorFileModel.objects.filter(faculty_answer=faculty_answer).first()

            data = {
                "assign_id": assignment.assign_id,
                "student_name": student_name,
                "student_file": student_file.assignment_file.url if student_file else None,
                "delivery_date": delivery_date,
                "faculty_answer_file": faculty_answer.answer_file.url if faculty_answer else None,
                "manager_error_file": manager_error.error_file.url if manager_error and manager_error.error_file else None,
            }

            response_data.append(data)

        if request.method == 'POST':
            if 'faculty-upload' in request.POST:
                assign_id = request.POST.get('assign_id')
                answer_file = request.FILES.get('answer_file')

                if assign_id and answer_file:
                    # Get the assignment object by its ID
                    assignment = get_object_or_404(FacultyAssignModel, assign_id=assign_id)

                    # Check if an answer already exists for this assignment
                    faculty_answer, created = FacultyAnswerModel.objects.get_or_create(
                        faculty=UserModel.objects.get(user_id = user),  # Assuming the faculty is the logged-in user
                        assigned_file=assignment,
                        defaults={
                            'answer_file': answer_file,
                            'uploaded_date': datetime.now(),
                            'status': 'Verifying'  # Default status when faculty uploads the file
                        }
                    )

                    # If the answer already exists, update the answer file and the uploaded date
                    if not created:
                        faculty_answer.answer_file = answer_file
                        faculty_answer.uploaded_date = datetime.now()
                        faculty_answer.status = 'Verifying'
                        faculty_answer.save()

        return render(request, 'faculty.html', {'username': username, 'uploaded_files': response_data})


def allfiles(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"
        usertype = UserType.objects.get(user_type='Manager')

        if loggedin_user.user_type == usertype:

            if request.method == 'POST':
                # Handle file upload or status change
                assign_id = request.POST.get('assign_id')
                status = request.POST.get('status')
                error_file = request.FILES.get('error_file')

                # Fetch the assignment object
                assignment = FacultyAssignModel.objects.get(assign_id=assign_id)

                if error_file:
                    # Handle error file upload
                    ManagerErrorFileModel.objects.create(
                        faculty_answer=FacultyAnswerModel.objects.get(assigned_file=assignment),
                        error_file=error_file,
                        uploaded_date=datetime.now(),
                        manager = UserModel.objects.get(user_id = user)
                    )

                if status:
                    answer_file = FacultyAnswerModel.objects.get(assigned_file =assignment)
                    # Update assignment status
                    answer_file.status = status
                    answer_file.save()

            # Get all the assignments
            assignments = FacultyAssignModel.objects.all()

            # Prepare the response data
            response_data = []

            for assignment in assignments:
                student_file = assignment.file
                student_name = f"{student_file.student.first_name} {student_file.student.last_name}"
                delivery_date = assignment.file.expected_delivery_date
                faculty_answer = FacultyAnswerModel.objects.filter(assigned_file=assignment).first()
                manager_error = ManagerErrorFileModel.objects.filter(faculty_answer=faculty_answer).first()

                data = {
                    "assign_id": assignment.assign_id,
                    "student_name": student_name,
                    "faculty_name": f"{assignment.assigned_to.first_name} {assignment.assigned_to.last_name}",
                    "student_file": student_file.assignment_file.url if student_file else None,
                    "delivery_date": delivery_date,
                    "faculty_answer_file": faculty_answer.answer_file.url if faculty_answer else None,
                    "answer_uploadedtime": faculty_answer.uploaded_date if faculty_answer else None,
                    "manager_error_file": manager_error.error_file.url if manager_error and manager_error.error_file else None,
                    "status": faculty_answer.status if faculty_answer else None,
                }

                response_data.append(data)
        else:

            if request.method == 'POST':
                # Handle file upload or status change
                assign_id = request.POST.get('assign_id')
                answerfile = request.FILES.get('answer_file')
                answer_file = FacultyAnswerModel.objects.get(assigned_file=assign_id)

                if answer_file:
                    answer_file.answer_file = answerfile
                    answer_file.uploaded_date = datetime.now()
                    answer_file.save()


            # Get all the assignments
            assignments = FacultyAssignModel.objects.filter(assigned_to=loggedin_user)

            # Prepare the response data
            response_data = []

            for assignment in assignments:
                student_file = assignment.file
                student_name = f"{student_file.student.first_name} {student_file.student.last_name}"
                delivery_date = assignment.file.expected_delivery_date
                faculty_answer = FacultyAnswerModel.objects.filter(assigned_file=assignment).first()
                manager_error = ManagerErrorFileModel.objects.filter(faculty_answer=faculty_answer).first()

                data = {
                    "assign_id": assignment.assign_id,
                    "student_name": student_name,
                    "student_file": student_file.assignment_file.url if student_file else None,
                    "delivery_date": delivery_date,
                    "faculty_answer_file": faculty_answer.answer_file.url if faculty_answer else None,
                    "manager_error_file": manager_error.error_file.url if manager_error and manager_error.error_file else None,
                    "status": faculty_answer.status if faculty_answer else None,
                }

                response_data.append(data)

    return render(request, 'allfiles.html', {'username': username, 'uploaded_files': response_data, 'user_type': loggedin_user.user_type.user_type})


def faculty_assign(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"
        response_data = []

        student_files = StudentFileModel.objects.all()
        for student_file in student_files:
            assigned = FacultyAssignModel.objects.get(file=student_file)

            data ={
                "file_id":student_file.studentfile_id,
                "student_name": f"{student_file.student.first_name} {student_file.student.last_name}",
                "student_file": student_file.assignment_file.url if student_file else None,
                "faculty": f"{assigned.assigned_to.first_name} {assigned.assigned_to.last_name}",
                "delivery_date": student_file.expected_delivery_date,

            }
            response_data.append(data)

    return render(request, 'assign_faculty.html', {'username': username, 'uploaded_files': response_data})


def all_users(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loggedin_user = UserModel.objects.get(user_id=user)
        username = f"{loggedin_user.first_name} {loggedin_user.last_name}"

        all_user = UserModel.objects.all()
    return render(request, 'all_users.html', {'username': username, 'all_users': all_user, 'user_type': loggedin_user.user_type.user_type})


def logout(request):
    del request.session['user']
    return redirect('/')



from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Enrollment

# Create your views here.

'''

@login_required
def student_grades(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course").prefetch_related(
        "grades__assessment_item__component"
    )

    return render(
        request,
        "enrollments/student_grades.html",
        {"enrollments": enrollments}
    )

'''



from django.contrib.auth.decorators import login_required

@login_required
def student_grades(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(
        request,
        "enrollments/student_grades.html",
        {"enrollments": enrollments}
    )



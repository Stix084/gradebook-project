from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.decorators import lecturer_required
from enrollments.models import Enrollment

from users.models import User


@lecturer_required
def enter_grades(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # all active students in this course
    enrollments = Enrollment.objects.filter(
        course=course,
        status="ACTIVE"
    ).select_related("student")

    students = [e.student for e in enrollments]

    assessments = course.assessments.all()

    if request.method == "POST":
        for student in students:
            for assessment in assessments:

                field_name = f"grade_{student.id}_{assessment.id}"
                score = request.POST.get(field_name)

                if score not in [None, ""]:
                    Grade.objects.update_or_create(
                        student=student,
                        assessment=assessment,
                        defaults={
                            "marks_obtained": score
                        }
                    )

        messages.success(request, "Grades saved successfully.")
        return redirect(request.path)

    context = {
        "course": course,
        "students": students,
        "assessments": assessments,
    }

    return render(request, "courses/enter_grades.html", context)
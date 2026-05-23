
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from courses.models import Course, Grade
from enrollments.models import Enrollment

@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    assessments = course.assessments.all()

    grades = Grade.objects.filter(
        student=request.user,
        assessment__course=course
    ).select_related("assessment")

    # Separate assignments from everything else
    assignments = [g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"]
    others = [g for g in grades if g.assessment.assessment_type != "ASSIGNMENT"]

    # Non-assignment contributions
    final_score = 0
    for g in others:
        if g.assessment.total_marks > 0:
            ratio = g.marks_obtained / g.assessment.total_marks
            final_score += ratio * g.assessment.weight

    # Assignment group contribution
    if assignments:
        total_obtained = sum(g.marks_obtained for g in assignments)
        total_possible = sum(g.assessment.total_marks for g in assignments)
        group_weight = assignments[0].assessment.weight
        if total_possible > 0:
            final_score += (total_obtained / total_possible) * group_weight

    return render(request, "courses/course_detail.html", {
        "course": course,
        "enrollment": enrollment,
        "assessments": assessments,
        "grades": grades,
        "final_score": final_score
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from courses.models import Course, Grade, Assessment
from enrollments.models import Enrollment


def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role == "STUDENT":
        return redirect("dashboard")
    return redirect("lecturer_dashboard")


@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")
    return render(request, "student/dashboard.html", {
        "enrollments": enrollments
    })


@login_required
def lecturer_dashboard(request):
    courses = Course.objects.filter(lecturer=request.user)
    return render(request, "lecturer/dashboard.html", {
        "courses": courses
    })


@login_required
def lecturer_course_summary(request, id):
    course = get_object_or_404(Course, id=id, lecturer=request.user)
    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related("student")

    assessments = list(course.assessments.all())
    non_assignments = [a for a in assessments if a.assessment_type != "ASSIGNMENT"]

    rows = []
    for enrollment in enrollments:
        student = enrollment.student
        grades = Grade.objects.filter(
            student=student,
            assessment__course=course
        ).select_related("assessment")

        grade_map = {g.assessment_id: g for g in grades}

        # Non-assignment marks
        non_assignment_marks = []
        for a in non_assignments:
            g = grade_map.get(a.id)
            non_assignment_marks.append(
                round(g.marks_obtained, 1) if g else "-"
            )

        # Assignment average
        assignment_grades = [
            g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"
        ]
        if assignment_grades:
            total_obtained = sum(g.marks_obtained for g in assignment_grades)
            total_possible = sum(g.assessment.total_marks for g in assignment_grades)
            avg = round((total_obtained / total_possible) * 100, 1) if total_possible > 0 else "-"
        else:
            avg = "-"

        # Final mark
        final = enrollment.final_mark()

        rows.append({
            "student": student,
            "non_assignment_marks": non_assignment_marks,
            "assignment_avg": avg,
            "final_mark": final,
        })

    return render(request, "lecturer/course_summary.html", {
        "course": course,
        "non_assignments": non_assignments,
        "rows": rows,
    })


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

    assignments = [g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"]
    others = [g for g in grades if g.assessment.assessment_type != "ASSIGNMENT"]

    final_score = 0
    for g in others:
        if g.assessment.total_marks > 0:
            ratio = g.marks_obtained / g.assessment.total_marks
            final_score += ratio * g.assessment.weight

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
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from courses.models import Course, Grade, Assessment
from enrollments.models import Enrollment
from courses.models import Course, Grade, Assessment, ClassLog
from django.utils.dateparse import parse_date
from courses.models import Course, Grade, Assessment, ClassLog, Submission 
import cloudinary.uploader

@login_required
def submit_assignment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    course = assessment.course

    # Only allow submissions for assignments
    if assessment.assessment_type != "ASSIGNMENT":
        return redirect("course_detail", id=course.id)

    # Check student is enrolled
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()
    if not enrollment:
        return redirect("dashboard")

    existing = Submission.objects.filter(
        student=request.user,
        assessment=assessment
    ).first()

    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if uploaded_file:
            result = cloudinary.uploader.upload(
                uploaded_file,
                resource_type="raw",
                folder=f"submissions/{course.code}/{assessment.id}/"
            )
            Submission.objects.update_or_create(
                student=request.user,
                assessment=assessment,
                defaults={
                    "file_url": result["secure_url"],
                    "file_name": uploaded_file.name,
                }
            )
            return redirect("course_detail", id=course.id)

    return render(request, "student/submit_assignment.html", {
        "assessment": assessment,
        "course": course,
        "existing": existing,
    })

#--------------------------------------------------------------
@login_required
def enter_grades(request, course_id, assessment_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user)
    assessment = get_object_or_404(Assessment, id=assessment_id, course=course)
    enrollments = Enrollment.objects.filter(course=course).select_related("student")

    errors = []

    if request.method == "POST":
        for enrollment in enrollments:
            student = enrollment.student
            mark_key = f"mark_{student.id}"
            mark_value = request.POST.get(mark_key, "").strip()

            if mark_value == "":
                continue

            try:
                mark = float(mark_value)
            except ValueError:
                errors.append(f"{student.username}: invalid mark '{mark_value}'")
                continue

            if mark > assessment.total_marks:
                errors.append(
                    f"{student.username}: mark {mark} exceeds total marks ({assessment.total_marks})"
                )
                continue

            if mark < 0:
                errors.append(f"{student.username}: mark cannot be negative")
                continue

            Grade.objects.update_or_create(
                student=student,
                assessment=assessment,
                defaults={"marks_obtained": mark}
            )

        if not errors:
            return redirect("lecturer_course_summary", id=course_id)

    # Build student rows with existing grades
    rows = []
    for enrollment in enrollments:
        student = enrollment.student
        existing = Grade.objects.filter(
            student=student,
            assessment=assessment
        ).first()
        rows.append({
            "student": student,
            "existing_mark": existing.marks_obtained if existing else "",
        })

    return render(request, "lecturer/enter_grades.html", {
        "course": course,
        "assessment": assessment,
        "rows": rows,
        "errors": errors,
    })


#--------------------------------------------------------------
@login_required
def class_log(request, id):
    course = get_object_or_404(Course, id=id, lecturer=request.user)

    # Handle new log
    if request.method == "POST" and "log_class" in request.POST:
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        duration = request.POST.get("duration")
        topic = request.POST.get("topic")
        notes = request.POST.get("notes", "")

        if date and topic and start_time and duration:
            ClassLog.objects.create(
                course=course,
                lecturer=request.user,
                date=parse_date(date),
                start_time=start_time,
                duration=duration,
                topic=topic,
                notes=notes
            )

    # Handle edit
    if request.method == "POST" and "edit_log" in request.POST:
        log_id = request.POST.get("log_id")
        log = get_object_or_404(ClassLog, id=log_id, lecturer=request.user)
        log.date = parse_date(request.POST.get("date"))
        log.start_time = request.POST.get("start_time")
        log.duration = request.POST.get("duration")
        log.topic = request.POST.get("topic")
        log.notes = request.POST.get("notes", "")
        log.save()

    # Handle delete
    if request.method == "POST" and "delete_log" in request.POST:
        log_id = request.POST.get("log_id")
        ClassLog.objects.filter(id=log_id, lecturer=request.user).delete()

    logs = ClassLog.objects.filter(course=course).order_by("-date")
    edit_log = None
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_log = get_object_or_404(ClassLog, id=edit_id, lecturer=request.user)

    return render(request, "lecturer/class_log.html", {
        "course": course,
        "logs": logs,
        "edit_log": edit_log,
    })

#--------------------------------------------------------------


def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role == "STUDENT":
        return redirect("dashboard")
    return redirect("lecturer_dashboard")



@login_required
def student_dashboard(request):
    if request.user.role != "STUDENT":
        return redirect("lecturer_dashboard")
    
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
        "assessments": assessments,
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
import openpyxl
from django.http import HttpResponse

@login_required
def export_course_summary(request, id):
    course = get_object_or_404(Course, id=id, lecturer=request.user)
    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related("student")

    assessments = list(course.assessments.all())
    non_assignments = [a for a in assessments if a.assessment_type != "ASSIGNMENT"]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = course.code

    # Header row
    headers = ["Student Number", "First Name", "Last Name"]
    for a in non_assignments:
        headers.append(a.title)
    headers += ["Assignments (avg)", "Final Mark"]
    ws.append(headers)

    # Data rows
    for enrollment in enrollments:
        student = enrollment.student
        grades = Grade.objects.filter(
            student=student,
            assessment__course=course
        ).select_related("assessment")

        grade_map = {g.assessment_id: g for g in grades}

        row = [
            student.student_number or "",
            student.first_name,
            student.last_name,
        ]

        for a in non_assignments:
            g = grade_map.get(a.id)
            row.append(g.marks_obtained if g else "-")

        assignment_grades = [
            g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"
        ]
        if assignment_grades:
            total_obtained = sum(g.marks_obtained for g in assignment_grades)
            total_possible = sum(g.assessment.total_marks for g in assignment_grades)
            avg = round((total_obtained / total_possible) * 100, 1) if total_possible > 0 else "-"
        else:
            avg = "-"

        row.append(avg)
        row.append(enrollment.final_mark())
        ws.append(row)

    # Return as download
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{course.code}_grade_summary.xlsx"'
    wb.save(response)
    return response

submissions = Submission.objects.filter(
    assessment=assessment
   ).select_related("student")

    return render(request, "lecturer/enter_grades.html", {
    "course": course,
    "assessment": assessment,
    "rows": rows,
    "errors": errors,
    "submissions": submissions,
    })


    
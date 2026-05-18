from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.decorators import lecturer_required
from enrollments.models import Enrollment
from courses.models import AssessmentItem, Grade

@lecturer_required
def enter_grades(request, course_id):
    enrollments = Enrollment.objects.filter(
        course_id=course_id,
        status="ACTIVE"
    ).select_related("student")

    assessment_items = AssessmentItem.objects.filter(
        component__course_id=course_id
    )

    if request.method == "POST":
        for enrollment in enrollments:
            for item in assessment_items:
                field_name = f"grade_{enrollment.id}_{item.id}"
                score = request.POST.get(field_name)

                if score is not None and score != "":
                    Grade.objects.update_or_create(
                        enrollment=enrollment,
                        assessment_item=item,
                        defaults={
                            "score": score,
                            "max_score": item.max_score
                        }
                    )

        messages.success(request, "Grades saved successfully.")
        return redirect(request.path)

    context = {
        "enrollments": enrollments,
        "assessment_items": assessment_items,
    }
    return render(request, "courses/enter_grades.html", context)


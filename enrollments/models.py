def final_mark(self):
    from courses.models import Grade
    grades = Grade.objects.filter(
        student=self.student,
        assessment__course=self.course
    ).select_related("assessment")

    final = 0

    # Separate assignments from everything else
    assignments = [g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"]
    others = [g for g in grades if g.assessment.assessment_type != "ASSIGNMENT"]

    # Non-assignment contributions (normal weighted calc)
    for g in others:
        if g.assessment.total_marks > 0:
            ratio = g.marks_obtained / g.assessment.total_marks
            final += ratio * g.assessment.weight

    # Assignment group contribution (average first, then apply weight)
    if assignments:
        total_obtained = sum(g.marks_obtained for g in assignments)
        total_possible = sum(g.assessment.total_marks for g in assignments)
        group_weight = assignments[0].assessment.weight
        if total_possible > 0:
            final += (total_obtained / total_possible) * group_weight

    return round(final, 1)
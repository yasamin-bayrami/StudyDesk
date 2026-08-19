from datetime import date


def is_overdue(due_date, completed):
    today = date.today().isoformat()

    if due_date == "":
        return False

    if due_date < today and not completed:
        return True

    return False
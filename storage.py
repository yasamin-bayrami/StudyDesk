import json

def save_assignments(assignments):
    with open("assignments.json", "w") as file:
        json.dump(assignments, file)


def load_assignments():
    try:
        with open("assignments.json", "r") as file:
            saved_assignments = json.load(file)
            return saved_assignments
    except FileNotFoundError:
        return []
import customtkinter as ctk
from tkcalendar import Calendar
from storage import save_assignments, load_assignments
from dates import is_overdue
from calendar_ui import open_calendar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("StudyDesk")
app.geometry("900x600")
main_frame = ctk.CTkScrollableFrame(
    master=app
)

main_frame.pack(
    fill="both",
    expand=True
)
title_label = ctk.CTkLabel(master=main_frame, text="StudyDesk", font=ctk.CTkFont(size=32, weight="bold"))
title_label.pack(pady=(40, 10))
instruction_label= ctk.CTkLabel(master=main_frame, text="Enter an assignment below:", font=ctk.CTkFont(size=16))
instruction_label.pack(pady=10)
assignment_entry = ctk.CTkEntry(master=main_frame, width=400, height=40, placeholder_text="Example: Complete math homework")
assignment_entry.pack(pady=10)

result_label = ctk.CTkLabel(master=main_frame, text="", font=ctk.CTkFont(size=16))
result_label.pack(pady=0)


    
def reset_assignments():
    assignments.clear()
    save_assignments(assignments)
    refresh_assignments()
    
assignments = load_assignments()

due_date_frame = ctk.CTkFrame(master=main_frame,fg_color="transparent")

def toggle_due_date():
    if use_due_date.get():
        due_date_frame.pack(
            pady=(5, 10),
            before=add_button
        )
    else:
        due_date_entry.delete(0, "end")
        due_date_frame.pack_forget()

calendar_button = ctk.CTkButton(
        master=due_date_frame,
        text="📅",
        width=45,
        height=40,
        command=lambda: open_calendar(app, due_date_entry)    )

calendar_button.grid(
        row=0,
        column=1
    )

use_due_date = ctk.BooleanVar(value=False)

due_date_checkbox = ctk.CTkCheckBox(master=main_frame,text="Add due date",variable=use_due_date,command=toggle_due_date)
due_date_checkbox.pack(pady=(2,2))


due_date_entry = ctk.CTkEntry(
    master=due_date_frame,
    width=340,
    height=40,
    placeholder_text="Due date: YYYY-MM-DD"
)

due_date_entry.grid(
    row=0,
    column=0,
    padx=(0, 5)
)

def add_assignment():
    assignment_text = assignment_entry.get()
    due_date_text = due_date_entry.get()
    if assignment_text == "":
        result_label.configure(text="Please enter an assignment first.")

    else:
        result_label.configure(text="")

        assignments.append({
            "text": assignment_text,
            "completed": False,
            "due_date": due_date_text
    })
    save_assignments(assignments)
    refresh_assignments()
    print(assignments)
    assignment_entry.delete(0, "end")
    due_date_entry.delete(0, "end")

def complete_assignment(assignment):
    assignment["completed"] = True
    save_assignments(assignments)
    refresh_assignments()

def delete_assignment(assignment):
    assignments.remove(assignment)
    save_assignments(assignments)
    refresh_assignments()

def refresh_assignments():
    for widget in assignments_frame.winfo_children():
        widget.destroy()

    for row_number, assignment in enumerate(assignments):
        

        assignment_row = ctk.CTkFrame(
           master=assignments_frame
        )

        assignment_row.pack(
            pady=5,
            padx=10
        )
        assignment_row.grid_columnconfigure(0, weight=1)

        due_date = assignment.get("due_date", "")

        if due_date == "":
            display_text = assignment["text"]

        elif is_overdue(due_date, assignment["completed"]):
            display_text = assignment["text"] + " — OVERDUE"

        else:
            display_text = assignment["text"] + " — Due: " + due_date
        assignment_label = ctk.CTkLabel(
            master=assignment_row,
            text=display_text
                   )
        
        assignment_label.grid(
                    row=0,
                    column=0,
                    padx=10,
                    pady=10,
                    sticky="w"
        )

        if assignment["completed"]:
            check_label = ctk.CTkLabel(
            master=assignment_row,
            text="✅"
            )

            check_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
            )

        else:
            complete_button = ctk.CTkButton(
            master=assignment_row,
            text="Complete",
            command=lambda current_assignment=assignment: complete_assignment(current_assignment)
            )

            complete_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
            )
        delete_button = ctk.CTkButton(
            master=assignment_row,
            text="Delete",
            command=lambda current_assignment=assignment: delete_assignment(current_assignment)
        )

        delete_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )
add_button = ctk.CTkButton(master=main_frame, text="Add Assignment", command=add_assignment)
add_button.pack(pady=10)

reset_button = ctk.CTkButton(
    master=main_frame,
    text="Reset Assignments",
    command=reset_assignments
)

reset_button.pack(pady=10)
assignments_frame = ctk.CTkFrame(master=main_frame)
assignments_frame.pack(
    pady=20
)
refresh_assignments()


app.mainloop()
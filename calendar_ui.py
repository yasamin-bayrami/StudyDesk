import customtkinter as ctk
from tkcalendar import Calendar

def open_calendar(app, due_date_entry):
    calendar_window = ctk.CTkToplevel(app)
    calendar_window.title("Choose Due Date")
    calendar_window.geometry("350x350")

    calendar = Calendar(
        calendar_window,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        font=("Arial", 14)
    )

    calendar.pack(padx=20, pady=20)
    def choose_date():
        selected_date = calendar.get_date()
        due_date_entry.delete(0, "end")
        due_date_entry.insert(0, selected_date)
        calendar_window.destroy()
    select_button = ctk.CTkButton(
        master=calendar_window,
        text="Use This Date",
        command=choose_date
    )

    select_button.pack(pady=(0, 20))
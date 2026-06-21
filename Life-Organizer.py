import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date


# =========================
# DATABASE
# =========================

conn = sqlite3.connect("life_tracker.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_entries (

id INTEGER PRIMARY KEY AUTOINCREMENT,

date TEXT,

chess_played REAL,
chess_studied REAL,
leetcode REAL,
language_learning REAL,
projects REAL,

calories INTEGER,
protein REAL,
gym INTEGER,
cardio_sports REAL,
cardio_walks REAL,
cardio_runs REAL,
abs INTEGER,
sleep REAL,
weight REAL,

philosophy_pages INTEGER,
girlfriend_time REAL,
family_time REAL,
friends_time REAL,
good_deeds REAL,
mood INTEGER,

work_hours REAL,
gf_discretionary REAL,
personal_discretionary REAL,
mixed_discretionary REAL,
gf_necessary REAL,
personal_necessary REAL,
mixed_necessary REAL,

youtube REAL,
anime REAL,
gaming REAL

)
""")


conn.commit()



# =========================
# FIELDS
# =========================

FIELDS = {

"Mind": [

("Chess Played (min)", "chess_played"),
("Chess Studied (min)", "chess_studied"),
("Leetcode (min)", "leetcode"),
("Language Learning (min)", "language_learning"),
("Independent Projects (min)", "projects")

],


"Body": [

("Calories (kcals)", "calories"),
("Protein (g)", "protein"),
("Gym", "gym"),
("Sports Cardio (min)", "cardio_sports"),
("Walk Cardio (min)", "cardio_walks"),
("Run Cardio (min)", "cardio_runs"),
("Abs", "abs"),
("Sleep (hrs)", "sleep"),
("Weight (kg)", "weight")

],


"Soul": [

("Philosophy Read (pages)", "philosophy_pages"),
("Girlfriend Time (hrs)", "girlfriend_time"),
("Family Time (hrs)", "family_time"),
("Friends Time (hrs)", "friends_time"),
("Good Deeds (min)", "good_deeds"),
("Mood (1-10)", "mood")

],


"Material": [

("Work Hours (hrs)", "work_hours"),

("GF Discretionary ($)", "gf_discretionary"),
("Personal Discretionary ($)", "personal_discretionary"),
("Mixed Discretionary ($)", "mixed_discretionary"),

("GF Necessary ($)", "gf_necessary"),
("Personal Necessary ($)", "personal_necessary"),
("Mixed Necessary ($)", "mixed_necessary")

],


"Hobby": [

("Approved YouTube (min)", "youtube"),
("Anime (min)", "anime"),
("Gaming (min)", "gaming")

]

}



entries = {}
checkboxes = {}



# =========================
# SAVE
# =========================

def save_entry():

    values = [
        date_var.get()
    ]


    for category in FIELDS:

        for label, db_name in FIELDS[category]:

            if db_name in checkboxes:

                values.append(
                    int(checkboxes[db_name].get())
                )

            else:

                value = entries[db_name].get()

                if value == "":
                    value = None

                values.append(value)



    cursor.execute("""
    INSERT INTO daily_entries VALUES
    (
    NULL,
    ?,

    ?,?,?,?,?,

    ?,?,?,?,?,?,?,?,?,

    ?,?,?,?,?,?,

    ?,?,?,?,?,?,?,

    ?,?,?

    )

    """, values)



    conn.commit()


    messagebox.showinfo(
        "Saved",
        "Daily entry saved"
    )

def show_history():

    history_window = tk.Toplevel(root)

    history_window.title("History")
    history_window.geometry("1400x500")


    columns = [
        "Date",

        "Chess Played",
        "Chess Studied",
        "Leetcode",
        "Language",
        "Projects",

        "Calories",
        "Protein",
        "Gym",
        "Sports",
        "Walks",
        "Runs",
        "Abs",
        "Sleep",
        "Weight",

        "Philosophy",
        "GF Time",
        "Family",
        "Friends",
        "Good Deeds",
        "Mood",

        "Work",

        "GF Disc",
        "Personal Disc",
        "Mixed Disc",
        "GF Necessary",
        "Personal Necessary",
        "Mixed Necessary",

        "YouTube",
        "Anime",
        "Gaming"
    ]


    tree = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )


    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            width=90
        )


    tree.pack(
        fill="both",
        expand=True
    )


    cursor.execute("""
        SELECT

        date,

        chess_played,
        chess_studied,
        leetcode,
        language_learning,
        projects,

        calories,
        protein,
        gym,
        cardio_sports,
        cardio_walks,
        cardio_runs,
        abs,
        sleep,
        weight,

        philosophy_pages,
        girlfriend_time,
        family_time,
        friends_time,
        good_deeds,
        mood,

        work_hours,

        gf_discretionary,
        personal_discretionary,
        mixed_discretionary,
        gf_necessary,
        personal_necessary,
        mixed_necessary,

        youtube,
        anime,
        gaming

        FROM daily_entries

        ORDER BY date DESC

    """)


    rows = cursor.fetchall()


    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )

# =========================
# GUI
# =========================

root = tk.Tk()

root.title("Life Tracker")
root.geometry("1350x600")


main = ttk.Frame(root)
main.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# Date

date_var = tk.StringVar(
    value=str(date.today())
)

ttk.Label(
    main,
    text="Date"
).grid(
    row=0,
    column=0,
    sticky="w"
)


ttk.Entry(
    main,
    textvariable=date_var
).grid(
    row=0,
    column=1
)



# Create 5 columns

categories = list(FIELDS.keys())


for col, category in enumerate(categories):


    section = ttk.LabelFrame(
        main,
        text=category,
        padding=10
    )

    section.grid(
        row=1,
        column=col,
        padx=10,
        pady=20,
        sticky="n"
    )


    for row,(label, db_name) in enumerate(FIELDS[category]):


        ttk.Label(
            section,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=3
        )


        if db_name in ["gym","abs"]:


            var = tk.BooleanVar()


            ttk.Checkbutton(
                section,
                variable=var
            ).grid(
                row=row,
                column=1
            )


            checkboxes[db_name]=var


        else:


            entry = ttk.Entry(
                section,
                width=12
            )


            entry.grid(
                row=row,
                column=1,
                padx=5
            )


            entries[db_name]=entry




# Save button

ttk.Button(
    root,
    text="Save Day",
    command=save_entry
).pack(
    pady=5
)


ttk.Button(
    root,
    text="View History",
    command=show_history
).pack(
    pady=5
)



root.mainloop()
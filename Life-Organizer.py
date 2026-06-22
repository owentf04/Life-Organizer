import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
gym REAL,
cardio_sports REAL,
cardio_walks REAL,
cardio_runs REAL,
abs REAL,
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
gaming REAL,

misc REAL
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
("Gym (min)", "gym"),
("Sports Cardio (min)", "cardio_sports"),
("Walk Cardio (min)", "cardio_walks"),
("Run Cardio (min)", "cardio_runs"),
("Abs (min)", "abs"),
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

],

"Misc": [
    ("Misc Time (min)", "misc")
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

    ?,?,?,

    ?
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
        "Gaming",

        "Misc"
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
        gaming,
                   
        misc

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

def show_dashboard():

    dashboard = tk.Toplevel(root)

    dashboard.title("Dashboard")

    dashboard.geometry("800x600")


    # Get latest day

    cursor.execute("""
        SELECT *

        FROM daily_entries

        ORDER BY date DESC

        LIMIT 1
    """)


    row = cursor.fetchone()


    if not row:

        messagebox.showinfo(
            "No Data",
            "No entries found"
        )

        return



    # Column mapping

    data = {

        "Mind": 0,
        "Body": 0,
        "Soul": 0,
        "Material": 0,
        "Hobby": 0,
        "Misc": 0

    }



    # -------------------
    # Mind (minutes)
    # -------------------

    data["Mind"] += (

        (row[2] or 0) +
        (row[3] or 0) +
        (row[4] or 0) +
        (row[5] or 0) +
        (row[6] or 0)
    ) / 60



    # -------------------
    # Body
    # -------------------

    data["Body"] += (
        (row[9] or 0) + # gym
        (row[10] or 0) + # sports
        (row[11] or 0) + # walks
        (row[12] or 0) + # runs
        (row[13] or 0)   # abs
    ) / 60


    # sleep is already hours

    data["Body"] += (
        row[14] or 0
    )



    # -------------------
    # Soul
    # -------------------

    data["Soul"] += (
        row[17] or 0
    )

    data["Soul"] += (
        row[18] or 0
    )

    data["Soul"] += (
        row[19] or 0
    )

    data["Soul"] += (
        row[20] or 0
    ) / 60



    # -------------------
    # Material
    # -------------------

    data["Material"] = (
        row[22] or 0
    )



    # -------------------
    # Hobby
    # -------------------

    data["Hobby"] += (
        (row[29] or 0) +
        (row[30] or 0) +
        (row[31] or 0)
    ) / 60

    data["Misc"] += (
        row[32] or 0
    ) / 60
    data

    # -------------------
    # Fill remaining time
    # -------------------

    total = sum(
        data.values()
    )


    if total < 24:

        data["Unaccounted"] = 24 - total



    labels = list(
        data.keys()
    )

    values = list(
        data.values()
    )



    # -------------------
    # Pie chart
    # -------------------

    fig = Figure(
        figsize=(6,6)
    )


    ax = fig.add_subplot(111)


    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )


    ax.set_title(
        "Most Recent Day Breakdown"
    )



    canvas = FigureCanvasTkAgg(
        fig,
        dashboard
    )


    canvas.draw()


    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

# =========================
# GUI
# =========================

root = tk.Tk()

root.title("Life Tracker")
root.geometry("1600x600")


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
    text="Dashboard",
    command=show_dashboard
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
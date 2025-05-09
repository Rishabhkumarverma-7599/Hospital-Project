from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector as c
from datetime import datetime
from tkinter.font import Font

# Database connection
try:
    mydb = c.connect(
        host="localhost",
        user="root",
        password="123456",
        database="hospitalDB",
        port=3306
    )
    mycursor = mydb.cursor()
except Exception as e:
    messagebox.showerror("Database Error", f"Failed to connect to MySQL:\n{e}")
    exit()

# Custom Colors
BG_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
BUTTON_HOVER = "#2980b9"
ACCENT_COLOR = "#e74c3c"
SUCCESS_COLOR = "#2ecc71"
TEXT_COLOR = "#ecf0f1"
ENTRY_BG = "#34495e"

# Fonts
TITLE_FONT = ("Helvetica", 20, "bold")
HEADING_FONT = ("Helvetica", 14, "bold")
BUTTON_FONT = ("Helvetica", 10, "bold")
LABEL_FONT = ("Helvetica", 10)

# Credentials
login_credentials = {
    "Patient": ("patient123", "pass1"),
    "Doctor": ("doctor123", "pass2"),
    "Lab Assistant": ("lab123", "pass3"),
    "Medicine": ("med123", "pass4"),
    "Visit": ("visit123", "pass5"),
    "Bill": ("bill123", "pass6"),
    "Lab Test": ("labtest123", "pass7"),
    "Admin": ("admin", "admin123"),
    "Update/Delete": ("update123", "pass8")
}

# Insert Data
def insert_data(table, fields, values):
    try:
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
        mycursor.execute(sql, values)
        mydb.commit()
        messagebox.showinfo("Success", f"Data inserted into {table} successfully.")
    except c.IntegrityError:
        messagebox.showerror("Duplicate Entry", "Primary key already exists.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert data:\n{e}")

# Edit Data
def edit_data(table, fields, values, primary_key_field, primary_key_value):
    try:
        set_clause = ', '.join([f"{field}=%s" for field in fields])
        sql = f"UPDATE {table} SET {set_clause} WHERE {primary_key_field} = %s"
        mycursor.execute(sql, values + [primary_key_value])
        mydb.commit()
        messagebox.showinfo("Success", f"Data in {table} updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update data:\n{e}")

# Delete Data
def delete_data(table, primary_key_field, primary_key_value):
    try:
        sql = f"DELETE FROM {table} WHERE {primary_key_field} = %s"
        mycursor.execute(sql, (primary_key_value,))
        mydb.commit()
        messagebox.showinfo("Success", f"Record deleted from {table}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete record:\n{e}")

# Data Entry Window
def open_window(title, labels, table, fields):
    win = Toplevel()
    win.title(title)
    win.geometry("500x600")
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    
    # Title Frame
    title_frame = Frame(win, bg=BG_COLOR)
    title_frame.pack(pady=10)
    
    Label(title_frame, text=title, font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Main Frame
    main_frame = Frame(win, bg=BG_COLOR)
    main_frame.pack(pady=10)

    entries = []
    for i, label in enumerate(labels):
        frame = Frame(main_frame, bg=BG_COLOR)
        frame.pack(pady=5)
        
        Label(frame, text=label, bg=BG_COLOR, fg=TEXT_COLOR, 
              font=LABEL_FONT, width=15, anchor="e").pack(side=LEFT, padx=5)
        
        var = StringVar()
        entry = Entry(frame, textvariable=var, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                     insertbackground=TEXT_COLOR, font=LABEL_FONT)
        entry.pack(side=LEFT, ipady=3)
        entries.append(var)

    # Button Frame
    button_frame = Frame(win, bg=BG_COLOR)
    button_frame.pack(pady=20)

    def submit():
        values = [e.get() for e in entries]
        if not all(values):
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return
        insert_data(table, fields, values)

    Button(button_frame, text="Insert", command=submit, bg=SUCCESS_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack(pady=5)

# Update/Delete Window
def open_update_delete_window(title, labels, table, fields):
    win = Toplevel()
    win.title(title)
    win.geometry("500x600")
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    
    # Title Frame
    title_frame = Frame(win, bg=BG_COLOR)
    title_frame.pack(pady=10)
    
    Label(title_frame, text=title, font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Main Frame
    main_frame = Frame(win, bg=BG_COLOR)
    main_frame.pack(pady=10)

    entries = []
    for i, label in enumerate(labels):
        frame = Frame(main_frame, bg=BG_COLOR)
        frame.pack(pady=5)
        
        Label(frame, text=label, bg=BG_COLOR, fg=TEXT_COLOR, 
              font=LABEL_FONT, width=15, anchor="e").pack(side=LEFT, padx=5)
        
        var = StringVar()
        entry = Entry(frame, textvariable=var, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                     insertbackground=TEXT_COLOR, font=LABEL_FONT)
        entry.pack(side=LEFT, ipady=3)
        entries.append(var)

    # Button Frame
    button_frame = Frame(win, bg=BG_COLOR)
    button_frame.pack(pady=20)

    def update():
        values = [e.get() for e in entries]
        if not all(values):
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return
        edit_data(table, fields[1:], values[1:], fields[0], values[0])

    def delete():
        key = entries[0].get()
        if not key:
            messagebox.showwarning("Missing Key", f"Please enter {fields[0]} to delete record.")
            return
        delete_data(table, fields[0], key)

    Button(button_frame, text="Update", command=update, bg=BUTTON_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack(side=LEFT, padx=10)
           
    Button(button_frame, text="Delete", command=delete, bg=ACCENT_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground="#c0392b",
           activeforeground=TEXT_COLOR).pack(side=LEFT, padx=10)

# Login Window
def login(section, labels, table, fields):
    login_win = Toplevel()
    login_win.title(f"{section} Login")
    login_win.geometry("350x300")
    login_win.configure(bg=BG_COLOR)
    login_win.resizable(False, False)
    
    # Title Frame
    title_frame = Frame(login_win, bg=BG_COLOR)
    title_frame.pack(pady=20)
    
    Label(title_frame, text=f"{section} Login", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Form Frame
    form_frame = Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=20)

    # Username
    Label(form_frame, text="Username", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    username = Entry(form_frame, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    username.grid(row=0, column=1, padx=5, pady=10)

    # Password
    Label(form_frame, text="Password", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    password = Entry(form_frame, show="*", bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    password.grid(row=1, column=1, padx=5, pady=10)

    # Button Frame
    button_frame = Frame(login_win, bg=BG_COLOR)
    button_frame.pack(pady=20)

    def check_login():
        user = username.get()
        pw = password.get()
        correct_user, correct_pass = login_credentials.get(section, ("", ""))
        if user == correct_user and pw == correct_pass:
            login_win.destroy()
            open_window(f"{section} Entry", labels, table, fields)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    Button(button_frame, text="Login", command=check_login, bg=BUTTON_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack()

# Update/Delete Login
def update_delete_login(section, labels, table, fields):
    login_win = Toplevel()
    login_win.title(f"{section} Login")
    login_win.geometry("350x300")
    login_win.configure(bg=BG_COLOR)
    login_win.resizable(False, False)
    
    # Title Frame
    title_frame = Frame(login_win, bg=BG_COLOR)
    title_frame.pack(pady=20)
    
    Label(title_frame, text=f"{section} Login", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Form Frame
    form_frame = Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=20)

    # Username
    Label(form_frame, text="Username", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    username = Entry(form_frame, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    username.grid(row=0, column=1, padx=5, pady=10)

    # Password
    Label(form_frame, text="Password", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    password = Entry(form_frame, show="*", bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    password.grid(row=1, column=1, padx=5, pady=10)

    # Button Frame
    button_frame = Frame(login_win, bg=BG_COLOR)
    button_frame.pack(pady=20)

    def check_login():
        user = username.get()
        pw = password.get()
        correct_user, correct_pass = login_credentials.get(section, ("", ""))
        if user == correct_user and pw == correct_pass:
            login_win.destroy()
            open_update_delete_window(f"{section} Operations", labels, table, fields)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    Button(button_frame, text="Login", command=check_login, bg=BUTTON_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack()

# Admin Login
def admin_login():
    admin_win = Toplevel()
    admin_win.title("Admin Login")
    admin_win.geometry("350x300")
    admin_win.configure(bg=BG_COLOR)
    admin_win.resizable(False, False)
    
    # Title Frame
    title_frame = Frame(admin_win, bg=BG_COLOR)
    title_frame.pack(pady=20)
    
    Label(title_frame, text="Admin Login", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Form Frame
    form_frame = Frame(admin_win, bg=BG_COLOR)
    form_frame.pack(pady=20)

    # Username
    Label(form_frame, text="Username", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    username = Entry(form_frame, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    username.grid(row=0, column=1, padx=5, pady=10)

    # Password
    Label(form_frame, text="Password", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    password = Entry(form_frame, show="*", bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                   insertbackground=TEXT_COLOR, font=LABEL_FONT)
    password.grid(row=1, column=1, padx=5, pady=10)

    # Button Frame
    button_frame = Frame(admin_win, bg=BG_COLOR)
    button_frame.pack(pady=20)

    def check_admin():
        if username.get() == login_credentials["Admin"][0] and password.get() == login_credentials["Admin"][1]:
            admin_win.destroy()
            retrieve_all()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    Button(button_frame, text="Login", command=check_admin, bg=SUCCESS_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=12, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack()

# Retrieve All with Filter
def retrieve_all():
    win = Toplevel()
    win.title("Database Summary")
    win.geometry("1000x700")
    win.configure(bg=BG_COLOR)
    
    # Title Frame
    title_frame = Frame(win, bg=BG_COLOR)
    title_frame.pack(pady=10)
    
    Label(title_frame, text="Hospital Database Summary", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()

    # Filter Frame
    filter_frame = Frame(win, bg=BG_COLOR)
    filter_frame.pack(pady=10)

    Label(filter_frame, text="Filter by Doctor or Date (YYYY-MM-DD):", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=LABEL_FONT).pack(side=LEFT, padx=5)
    
    filter_entry = Entry(filter_frame, bd=2, bg=ENTRY_BG, fg=TEXT_COLOR, 
                       insertbackground=TEXT_COLOR, font=LABEL_FONT, width=30)
    filter_entry.pack(side=LEFT, padx=5)
    filter_entry.insert(0, "Date")

    # Main Frame
    main_frame = Frame(win, bg=BG_COLOR)
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    canvas = Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def populate_tables(filter_text=""):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        tables = ["Patient", "Doctor", "Lab_Assistant", "Medicine", "Visit", "Bill", "Lab_Test"]
        for table in tables:
            try:
                query = f"SELECT * FROM {table}"
                if filter_text:
                    if table == "Doctor" and filter_text.lower() in ["doctor", "dr"]:
                        query += f" WHERE name LIKE '%{filter_text}%'"
                    elif table in ["Visit", "Bill"]:
                        query += f" WHERE timestamp LIKE '{filter_text}%'"

                mycursor.execute(query)
                rows = mycursor.fetchall()
                columns = [desc[0] for desc in mycursor.description]

                # Table Frame
                table_frame = Frame(scrollable_frame, bg=BG_COLOR)
                table_frame.pack(fill=X, pady=10)
                
                Label(table_frame, text=f"{table} Table", font=HEADING_FONT, 
                      bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 5))
                
                # Treeview with style
                style = ttk.Style()
                style.theme_use("clam")
                style.configure("Treeview", 
                              background=ENTRY_BG,
                              foreground=TEXT_COLOR,
                              fieldbackground=ENTRY_BG,
                              font=LABEL_FONT)
                style.configure("Treeview.Heading", 
                              background=BUTTON_COLOR,
                              foreground=TEXT_COLOR,
                              font=BUTTON_FONT)
                style.map("Treeview", background=[('selected', BUTTON_HOVER)])

                tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=min(5, len(rows)))
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120, anchor="center")

                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill=X)
            except Exception as e:
                Label(scrollable_frame, text=f"Error fetching {table}: {e}", 
                      fg=ACCENT_COLOR, bg=BG_COLOR).pack()

    def apply_filter():
        value = filter_entry.get().strip()
        populate_tables(value)

    Button(filter_frame, text="Filter", command=apply_filter, bg=BUTTON_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=10, bd=0, activebackground=BUTTON_HOVER,
           activeforeground=TEXT_COLOR).pack(side=LEFT, padx=5)
           
    Button(filter_frame, text="Clear", command=lambda: populate_tables(), bg=ACCENT_COLOR, fg=TEXT_COLOR, 
           font=BUTTON_FONT, width=10, bd=0, activebackground="#c0392b",
           activeforeground=TEXT_COLOR).pack(side=LEFT, padx=5)

    populate_tables()

# Main GUI
root = Tk()
root.title("Hospital Management System")
root.geometry("650x800")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Title Frame
title_frame = Frame(root, bg=BG_COLOR)
title_frame.pack(pady=20)

Label(title_frame, text="Hospital Management System", font=TITLE_FONT, 
      bg=BG_COLOR, fg=TEXT_COLOR).pack()

# Main Frame
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(pady=20)

# Sections
sections = [
    ("Patient", ["Patient ID", "Name", "Age", "Gender", "Email", "Aadhaar"], 
     "Patient", ["p_id", "name", "age", "gender", "email", "aadhaar"]),
    ("Doctor", ["Doctor ID", "Name", "Specialization"], 
     "Doctor", ["d_id", "name", "specification"]),
    ("Lab Assistant", ["Assistant ID", "Name", "Patient Name"], 
     "Lab_Assistant", ["s_id", "name", "patient_name"]),
    ("Medicine", ["Code", "Name", "Patient ID"], 
     "Medicine", ["code", "name", "code"]),
    ("Visit", ["Patient ID", "Doctor ID", "Problem", "Disease", "Treatment", "Time Stamp"], 
     "Visit", ["p_id", "d_id", "problem", "disease", "treatment", "timestamp"]),
    ("Bill", ["Bill ID", "Patient ID", "Patient Name", "Total Cost", "Medicine Code", "Date"], 
     "Bill", ["b_id", "p_id", "p_name", "cost", "code", "timestamp"]),
    ("Lab Test", ["Patient ID", "Test", "Result"], 
     "Lab_Test", ["p_id", "test", "result"])
]

update_delete_sections = [
    ("Patient Update/Delete", ["Patient ID", "Name", "Age", "Gender", "Email", "Aadhaar"], 
     "Patient", ["p_id", "name", "age", "gender", "email", "aadhaar"]),
    ("Doctor Update/Delete", ["Doctor ID", "Name", "Specialization"], 
     "Doctor", ["d_id", "name", "specification"]),
    ("Lab Assistant Update/Delete", ["Assistant ID", "Name", "Patient Name"], 
     "Lab_Assistant", ["s_id", "name", "patient_name"]),
    ("Medicine Update/Delete", ["Code", "Name", "Patient ID"], 
     "Medicine", ["code", "name", "code"]),
    ("Visit Update/Delete", ["Patient ID", "Doctor ID", "Problem", "Disease", "Treatment", "Time Stamp"], 
     "Visit", ["p_id", "d_id", "problem", "disease", "treatment", "timestamp"]),
    ("Bill Update/Delete", ["Bill ID", "Patient ID", "Patient Name", "Total Cost", "Medicine Code", "Date"], 
     "Bill", ["b_id", "p_id", "p_name", "cost", "code", "timestamp"]),
    ("Lab Test Update/Delete", ["Patient ID", "Test", "Result"], 
     "Lab_Test", ["p_id", "test", "result"])
]

# Create buttons for each section
for sec in sections:
    Button(main_frame, text=sec[0], command=lambda s=sec: login(*s), 
           bg=BUTTON_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT, width=25, bd=0,
           activebackground=BUTTON_HOVER, activeforeground=TEXT_COLOR).pack(pady=8)

# Update/Delete Button
Button(main_frame, text="Update/Delete Operations", 
       command=lambda: update_delete_login("Update/Delete", 
       update_delete_sections[0][1], update_delete_sections[0][2], update_delete_sections[0][3]), 
       bg="#f39c12", fg=TEXT_COLOR, font=BUTTON_FONT, width=25, bd=0,
       activebackground="#e67e22", activeforeground=TEXT_COLOR).pack(pady=8)

# Admin Button
Button(main_frame, text="Retrieve Full Database", command=admin_login, 
       bg=SUCCESS_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT, width=25, bd=0,
       activebackground="#27ae60", activeforeground=TEXT_COLOR).pack(pady=20)

root.mainloop()

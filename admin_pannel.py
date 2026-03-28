from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Admin_Pannel_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("1350x700+80+120")
        self.root.config(bg="white")

        # ------------Heading-------------
        Label(self.root, text="Users Table",
              font=("goudy old style", 22, "bold"),
              bg="#033054", fg="white").place(x=0, y=0, relwidth=1, height=50)

        # ------------Search-------------
        self.var_search = StringVar()

        Label(self.root, text="Search By Name:",
              font=("goudy old style", 15, "bold"),
              bg="white").place(x=280, y=75)

        Entry(self.root, textvariable=self.var_search,
              font=("goudy old style", 15),
              bg="lightyellow").place(x=450, y=75, width=200)

        Button(self.root, text="Search",
               font=("goudy old style", 15, "bold"),
               bg="#03a9f4", fg="white",cursor="hand2",
               command=self.search).place(x=670, y=73, width=120, height=30)

        # ------------Table Frame-------------
        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.place(x=150, y=130, width=970, height=450)

        # ------------Scrollbars-------------
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        # ------------Table-------------
        self.UsersTable = ttk.Treeview(
            table_frame,
            columns=("uid", "fname", "lname", "contact", "email", "question", "answer", "password"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        # ------------Placement-------------
        self.UsersTable.place(x=0, y=0, width=950, height=430)
        scrolly.place(x=950, y=0, width=20, height=430)
        scrollx.place(x=0, y=430, width=950, height=20)

        scrolly.config(command=self.UsersTable.yview)
        scrollx.config(command=self.UsersTable.xview)

        # ------------Headings-------------
        self.UsersTable.heading("uid", text="UID")
        self.UsersTable.heading("fname", text="First Name")
        self.UsersTable.heading("lname", text="Last Name")
        self.UsersTable.heading("contact", text="Contact")
        self.UsersTable.heading("email", text="Email")
        self.UsersTable.heading("question", text="Question")
        self.UsersTable.heading("answer", text="Answer")
        self.UsersTable.heading("password", text="Password")

        self.UsersTable["show"] = "headings"

        # ------------Column Size-------------
        self.UsersTable.column("uid", width=60)
        self.UsersTable.column("fname", width=120)
        self.UsersTable.column("lname", width=120)
        self.UsersTable.column("contact", width=100)
        self.UsersTable.column("email", width=180)
        self.UsersTable.column("question", width=120)
        self.UsersTable.column("answer", width=120)
        self.UsersTable.column("password", width=120)

        self.show()

    # --------Search---------
    def search(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get().strip() == "":
                messagebox.showerror("Error", "Enter name to search", parent=self.root)
                return

            cur.execute("""
                SELECT * FROM Users 
                WHERE f_name LIKE ? OR l_name LIKE ?
            """, ("%" + self.var_search.get() + "%", "%" + self.var_search.get() + "%"))

            rows = cur.fetchall()
            self.UsersTable.delete(*self.UsersTable.get_children())

            if rows:
                for row in rows:
                    self.UsersTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"{str(ex)}")
        finally:
            con.close()

    # --------Show---------
    def show(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM Users")
            rows = cur.fetchall()

            self.UsersTable.delete(*self.UsersTable.get_children())

            if rows:
                for row in rows:
                    self.UsersTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No data available", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"{str(ex)}")
        finally:
            con.close()


# --------Run---------
root = Tk()
obj = Admin_Pannel_Window(root)
root.mainloop()
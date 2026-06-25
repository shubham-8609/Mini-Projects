import tkinter as tk

from tkinter import messagebox

from manager import Manager


class LoginWindow:

    def __init__(self):

        self.manager = Manager()

        self.window = tk.Tk()

        self.window.title("Bank Management System")

        self.window.geometry("500x400")

        self.window.resizable(False, False)

        # -------------------------

        title = tk.Label(

            self.window,

            text="Bank Management System",

            font=("Arial", 18, "bold")

        )

        title.pack(pady=20)

        # -------------------------

        tk.Label(

            self.window,

            text="Username"

        ).pack()

        self.username_entry = tk.Entry(

            self.window,

            width=30

        )

        self.username_entry.pack()

        # -------------------------

        tk.Label(

            self.window,

            text="Password"

        ).pack(pady=(15, 0))

        self.password_entry = tk.Entry(

            self.window,

            show="*",

            width=30

        )

        self.password_entry.pack()

        # -------------------------

        login_button = tk.Button(

            self.window,

            text="Login",

            width=20,

            command=self.login

        )

        login_button.pack(pady=15)

        # -------------------------

        register_button = tk.Button(

            self.window,

            text="Register",

            width=20,

            command=self.register

        )

        register_button.pack()

    # ---------------------------------

    def login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()

        user = self.manager.login(

            username,

            password

        )

        if user:

            messagebox.showinfo(

                "Success",

                "Login Successful"

            )

            print(user)

        else:

            messagebox.showerror(

                "Error",

                "Invalid Username or Password"

            )

    # ---------------------------------

    def register(self):

        messagebox.showinfo(

            "Coming Soon",

            "Registration Window"

        )

    # ---------------------------------

    def run(self):

        self.window.mainloop()
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from database import DB
from api import Api
import os


class NLPapp:
    def __init__(self):
        self.api = Api()
        self.dbo = DB()

        self.root = Tk()
        self.root.title("Weather Application")
        self.root.geometry('400x600')
        self.root.configure(bg="#2C3E50")

        self.login_gui()
        self.root.mainloop()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGO ----------------
    def logo(self):
        logo_path = "logo.png"

        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(img)

            logo_label = Label(self.root, image=self.logo_img, bg="#2C3E50")
            logo_label.pack(pady=(15, 5))

        else:
            title = Label(self.root, text="Weather App", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 24, "bold"))
            title.pack(pady=(15, 5))

    # -------------- ENTRY WITH ICON ----------------
    def create_input_with_icon(self, icon_path, hide=False):
        frame = Frame(self.root, bg="#2C3E50")
        frame.pack(pady=10)

        img = Image.open(icon_path)
        img = img.resize((28, 28))
        icon = ImageTk.PhotoImage(img)

        icon_label = Label(frame, image=icon, bg="#2C3E50")
        icon_label.image = icon
        icon_label.pack(side=LEFT, padx=10)

        entry = Entry(frame, width=25, font=("Arial", 14))
        entry.pack(side=LEFT, ipady=6)

        if hide:
            entry.config(show="*")

        return entry

    # ---------------- LOGIN PAGE ----------------
    def login_gui(self):
        self.clear()
        self.logo()

        heading = Label(self.root, text='Weather Application', bg='#2C3E50', fg='#ECF0F1', font=('Arial', 22, 'bold'))
        heading.pack(pady=(20, 20))

        self.email_input = self.create_input_with_icon("email.png")
        self.password_input = self.create_input_with_icon("password.png", hide=True)

        login_btn = Button(self.root, text="Login", width=18,command=self.perform_login,bg="#27AE60", fg='white',font=("Arial", 14, "bold"))
        login_btn.pack(pady=(10, 5))

        member_login = Label(self.root, text="Not a member?",bg="#2C3E50", fg="white",font=("Arial", 14))
        member_login.pack(pady=(20, 10))

        register_btn = Button(self.root, text="Register", width=18,command=self.register,bg="#E74C3C", fg='white',font=("Arial", 14, "bold"))
        register_btn.pack(pady=(5, 20))

    def perform_login(self):
        email = self.email_input.get().strip()
        password = self.password_input.get().strip()

        if email == "" or password == "":
            messagebox.showerror("Error", "Email and Password cannot be empty!")
            return

        response = self.dbo.check_login(email, password)

        if response == 1:
            messagebox.showinfo("Success", "Login successful")
            self.home()
        elif response == 0:
            messagebox.showerror("Failed", "Incorrect password")
        else:
            messagebox.showerror("Failed", "Email not registered")

    # ---------------- REGISTER PAGE ----------------
    def register(self):
        self.clear()
        self.logo()

        heading = Label(self.root, text='Create Account',bg='#2C3E50', fg='#ECF0F1',font=('Arial', 22, 'bold'))
        heading.pack(pady=(20, 20))

        self.username_input = self.create_input_with_icon("user.png")
        self.email_input = self.create_input_with_icon("email.png")
        self.password_input = self.create_input_with_icon("password.png", hide=True)

        register_btn = Button(self.root, text="Register", width=18,command=self.perform_registration,bg="#E74C3C", fg='white',font=("Arial", 14, "bold"))
        register_btn.pack(pady=(10, 5))

        member_login = Label(self.root, text="Already a member?",bg="#2C3E50", fg="white",font=("Arial", 14))
        member_login.pack(pady=(20, 10))

        login_btn = Button(self.root, text="Login", width=18,command=self.login_gui,bg="#27AE60", fg='white',font=("Arial", 14, "bold"))
        login_btn.pack(pady=(5, 20))

    def perform_registration(self):
        username = self.username_input.get().strip()
        email = self.email_input.get().strip()
        password = self.password_input.get().strip()

        if username == "" or email == "" or password == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        response = self.dbo.register_user(username, email, password)

        if response == 1:
            messagebox.showinfo("Success", "Registration successful")
            self.login_gui()
        elif response == 0:
            messagebox.showerror("Failed", "Email already exists")
        else:
            messagebox.showerror("Error", "Something went wrong! Try again later.")

    # ---------------- HOME PAGE ----------------
    def home(self):
        self.clear()
        self.logo()

        heading = Label(self.root, text='Weather Application',bg='#2C3E50', fg='#ECF0F1',font=('Arial', 22, 'bold'))
        heading.pack(pady=(40, 40))

        search_btn = Button(self.root, text="Search by City Name",width=22, height=2,command=self.using_city_name,bg="#3498DB", fg='white',font=("Arial", 16, "bold"))
        search_btn.pack(pady=10)

        logout_btn = Button(self.root, text="Logout",width=16, height=1,command=self.login_gui,bg="#E74C3C", fg='white',font=("Arial", 12, "bold"))
        logout_btn.pack(pady=20)

    # ---------------- CITY WEATHER ----------------
    def using_city_name(self):
        self.clear()
        self.logo()

        heading = Label(self.root, text='Search Weather',bg='#2C3E50', fg='#ECF0F1',font=('Arial', 22, 'bold'))
        heading.pack(pady=(10, 20))

        city_label = Label(self.root, text="Enter city name",bg='#2C3E50', fg='#ECF0F1',font=("Arial", 14))
        city_label.pack(pady=5)

        self.city_input = Entry(self.root, width=25, font=("Arial", 14))
        self.city_input.pack(pady=10, ipady=5)

        search_btn = Button(self.root, text="Search", width=10,command=self.display_info,bg="#27AE60", fg='white',font=("Arial", 14, "bold"))
        search_btn.pack(pady=10)

        self.result = Text(self.root, width=40, height=12, wrap=WORD,bg='#2C3E50', fg='#ECF0F1', font=("Arial", 12))
        self.result.pack(pady=10)

        back_btn = Button(self.root, text="Back", width=10,command=self.home,bg="#E74C3C", fg="white",font=("Arial", 12, "bold"))
        back_btn.pack(pady=10)

    def display_info(self):
        city = self.city_input.get().strip()

        if city == "":
            messagebox.showerror("Error", "City name cannot be empty!")
            return

        data = self.api.get_info_by_city_name(city)

        self.result.config(state=NORMAL)
        self.result.delete(1.0, END)

        if "error" in data:
            self.result.insert(END, data["error"])
        else:
            self.result.insert(END, f"Weather Information:\n")
            self.result.insert(END, f"City: {city}\n")
            self.result.insert(END, f"Temperature: {data['current_temperature']}\n")
            self.result.insert(END, f"Weather: {data['weather']}\n")
            self.result.insert(END, f"Humidity: {data['humidity']}\n")
            self.result.insert(END, f"Sunrise: {data['sunrise']}\n")
            self.result.insert(END, f"Sunset: {data['sunset']}\n")
            self.result.insert(END, f"Country: {data['country']}\n")

        self.result.config(state=DISABLED)


if __name__ == "__main__":
    NLPapp()

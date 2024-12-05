#Importing dictionairies
import pickle
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

#Ticket Class
class Ticket:
    def __init__(self, ticket_id, ticket_type, price, validity, features, discount=0):
        self.__id = ticket_id
        self.__type = ticket_type
        self.__price = price
        self.__validity = validity
        self.__features = features
        self.__discount = discount

    # Getters and Setters
    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_price(self):
        return self.__price

    def get_validity(self):
        return self.__validity

    def get_features(self):
        return self.__features

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    # Methods
    def calculate_discounted_price(self):
        return self.__price * (1 - self.__discount / 100)

    def view_details(self):
        return {
            "id": self.__id,
            "type": self.__type,
            "price": self.__price,
            "validity": self.__validity,
            "features": self.__features,
            "discount": self.__discount,
        }

# Specialized Ticket Classes
class SingleDayPass(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(ticket_id, "Single Day Pass", price, "1 Day", "Valid only on selected date")

class TwoDayPass(Ticket):
    def __init__(self, ticket_id, price, discount=10):
        super().__init__(ticket_id, "Two Day Pass", price, "2 Days", "Cannot be split over multiple trips", discount)

class AnnualMembership(Ticket):
    def __init__(self, ticket_id, price, discount=15):
        super().__init__(ticket_id, "Annual Membership", price, "1 Year", "Must be used by the same person", discount)

class ChildTicket(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(ticket_id, "Child Ticket", price, "1 Day", "Must be accompanied by an adult")

class GroupTicket(Ticket):
    def __init__(self, ticket_id, price, discount=20):
        super().__init__(ticket_id, "Group Ticket", price, "1 Day", "Must be booked in advance", discount)

class VIPExperiencePass(Ticket):
    def __init__(self, ticket_id, price):
        super().__init__(ticket_id, "VIP Experience Pass", price, "1 Day", "Limited availability")

# UserAccount Class
class UserAccount:
    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__purchase_history = []

    def get_username(self):
        return self.__username

    def login(self, username, password):
        return self.__username == username and self.__password == password

    def add_to_history(self, order):
        self.__purchase_history.append(order)

    def view_order_history(self):
        return [order.view_order() for order in self.__purchase_history]

# Order Class
class Order:
    def __init__(self, order_id, ticket, total_amount):
        self.__order_id = order_id
        self.__ticket = ticket
        self.__total_amount = total_amount
        self.__date = datetime.now()
        self.__payment_status = False

    def make_payment(self):
        self.__payment_status = True

    def view_order(self):
        return {
            "order_id": self.__order_id,
            "ticket": self.__ticket.view_details(),
            "total_amount": self.__total_amount,
            "date": self.__date,
            "status": "Paid" if self.__payment_status else "Unpaid",
        }

# GUI Application
class TicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Booking System")
        self.system_data = {"users": [], "tickets": []}
        self.current_user = None
        self.load_data()
        if not self.system_data["tickets"]:
            self.add_sample_tickets()
        self.login_screen()

    def add_sample_tickets(self):
        self.system_data["tickets"].extend([
            SingleDayPass("T001", 275),
            TwoDayPass("T002", 480),
            AnnualMembership("T003", 1840),
            ChildTicket("T004", 185),
            GroupTicket("T005", 220),
            VIPExperiencePass("T006", 550)
        ])
        self.save_data()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.verify_login).pack()
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        for user in self.system_data["users"]:
            if user.login(username, password):
                self.current_user = user
                self.ticket_selection_screen()
                return
        messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Username").pack()
        self.new_username = tk.Entry(self.root)
        self.new_username.pack()
        tk.Label(self.root, text="Email").pack()
        self.new_email = tk.Entry(self.root)
        self.new_email.pack()
        tk.Label(self.root, text="Password").pack()
        self.new_password = tk.Entry(self.root, show="*")
        self.new_password.pack()
        tk.Button(self.root, text="Register", command=self.register_user).pack()
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def register_user(self):
        username = self.new_username.get()
        email = self.new_email.get()
        password = self.new_password.get()
        user = UserAccount(username, email, password)
        self.system_data["users"].append(user)
        self.save_data()
        messagebox.showinfo("Registration Successful", "You can now log in.")
        self.login_screen()

    def ticket_selection_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Select a Ticket").pack()
        for ticket in self.system_data["tickets"]:
            tk.Button(
                self.root,
                text=f"{ticket.get_type()} - ${ticket.calculate_discounted_price()} ({ticket.get_discount()}% off)",
                command=lambda t=ticket: self.purchase_ticket_screen(t),
            ).pack()
        tk.Button(self.root, text="View Order History", command=self.view_order_history).pack()

    def purchase_ticket_screen(self, ticket):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Ticket: {ticket.get_type()}").pack()
        tk.Label(self.root, text=f"Price: ${ticket.get_price()}").pack()
        tk.Label(self.root, text=f"Discount: {ticket.get_discount()}%").pack()
        tk.Label(self.root, text=f"Final Price: ${ticket.calculate_discounted_price()}").pack()
        tk.Label(self.root, text=f"Features: {ticket.get_features()}").pack()
        tk.Button(self.root, text="Confirm Purchase", command=lambda: self.complete_purchase(ticket)).pack()

    def complete_purchase(self, ticket):
        order = Order("O001", ticket, ticket.calculate_discounted_price())
        order.make_payment()
        self.current_user.add_to_history(order)
        self.save_data()
        messagebox.showinfo("Success", "Ticket Purchased Successfully!")
        self.ticket_selection_screen()

    def view_order_history(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Order History").pack()
        for order in self.current_user.view_order_history():
            details = order
            tk.Label(self.root, text=f"Order ID: {details['order_id']} - {details['ticket']['type']} - Status: {details['status']}").pack()
        tk.Button(self.root, text="Back", command=self.ticket_selection_screen).pack()

    def save_data(self):
        with open("system_data.pkl", "wb") as file:
            pickle.dump(self.system_data, file)

    def load_data(self):
        try:
            with open("system_data.pkl", "rb") as file:
                self.system_data = pickle.load(file)
        except FileNotFoundError:
            self.system_data = {"users": [], "tickets": []}

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()
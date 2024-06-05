import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class HotelBookingApp:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Hotel Booking Service")
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.label = tk.Label(self.main_frame, text="Вітаємо Hotel Booking Service!", font=("Arial", 16))
        self.label.pack(pady=10)

        self.login_button = tk.Button(self.main_frame, text="Авторизуватись", command=self.show_login, font=("Arial", 14))
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.main_frame, text="Зареєструватись", command=self.show_register, font=("Arial", 14))
        self.register_button.pack(pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack()

    def go_back_to_widgets(self):
        self.main_frame.pack_forget()
        self.clear_frame()
        self.create_widgets()

    def go_to_user_menu(self, client):
        self.main_frame.pack_forget()
        self.clear_frame()
        self.show_user_menu(client)

    def show_login(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Email:", font=("Arial", 14)).pack(pady=5)
        self.email_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.email_entry.pack()
        tk.Label(self.main_frame, text="Пароль:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.password_entry.pack()
        tk.Button(self.main_frame, text="Авторизуватись", command=self.login, font=("Arial", 14)).pack(pady=10)
        self.back_button = tk.Button(self.main_frame, text="Повернутись назад", command=self.go_back_to_widgets, font=("Arial", 14))
        self.back_button.pack()
        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=2)

    def show_register(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Ім'я:", font=("Arial", 14)).pack()
        self.first_name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.first_name_entry.pack()
        tk.Label(self.main_frame, text="Прізвище:", font=("Arial", 14)).pack()
        self.last_name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.last_name_entry.pack()
        tk.Label(self.main_frame, text="Email:", font=("Arial", 14)).pack()
        self.email_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.email_entry.pack()
        tk.Label(self.main_frame, text="Пароль:", font=("Arial", 14)).pack()
        self.password_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.password_entry.pack()
        self.admin_var = tk.BooleanVar()
        self.admin_checkbutton = tk.Checkbutton(self.main_frame, text="Я адмін", variable=self.admin_var,
                                                font=("Arial", 14))
        self.admin_checkbutton.pack()
        tk.Button(self.main_frame, text="Зареєструватись", command=self.register, font=("Arial", 14)).pack()
        self.back_button = tk.Button(self.main_frame, text="Повернутись назад", command=self.go_back_to_widgets,
                                     font=("Arial", 14))
        self.back_button.pack()
        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack()

    def exit(self):
        exit()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        client = self.controller.find_client_by_email(email)
        if client:
            if password == client.password:
                messagebox.showinfo("Авторизація", "Авторизація пройшла успішно!")
                self.show_user_menu(client)
                self.controller.logged_in_client = client
            else:
                messagebox.showerror("Авторизація", "Ви ввели неправильний пароль!")
        else:
            messagebox.showerror("Login", "Користувач не знайдений!")

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.admin_var.get() == True:
            is_admin = True
        else:
            is_admin = False
        client = self.controller.add_client(first_name, last_name, email, password, is_admin)
        messagebox.showinfo("Реєстрація", "Реєстрація пройшла успішно!")
        self.show_user_menu(client)

    def show_user_menu(self, client):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Вітаю {client.first_name} {client.last_name}!", font=("Arial", 16)).pack(pady=5)
        tk.Button(self.main_frame, text="Подивитись готелі", command=lambda: self.view_hotels(client), font=("Arial", 14)).pack(pady=5)
        if not client.is_admin:
            tk.Button(self.main_frame, text="Забронювати кімнату", command=lambda: self.show_booking_form(client), font=("Arial", 14)).pack(pady=5)
        tk.Button(self.main_frame, text="Подивитись броні", command=lambda: self.view_client_bookings(client), font=("Arial", 14)).pack(pady=5)
        if client.is_admin:
            self.button_show_list_of_clients = tk.Button(self.main_frame, text="Список користувачів", font=("Arial", 14))
            self.button_show_list_of_clients.pack(pady=5)
            self.button_show_list_of_clients.bind("<Button-1>", self.user_list_window)

        self.back_button = tk.Button(self.main_frame, text="Повернутись назад", command=self.go_back_to_widgets, font=("Arial", 14))
        self.back_button.pack(pady=5)
        tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14)).pack(pady=5)

    def view_hotels(self, client):
        self.clear_frame()
        self.hotels_text = tk.Label(self.main_frame, text="Список готелів", font=("Arial", 14))
        self.hotels_text.pack(anchor=tk.S, pady=5)
        self.hotel_listbox = tk.Listbox(self.main_frame, width=73)
        self.hotel_listbox.pack(anchor=tk.S, pady=15)
        self.hotel_listbox.bind("<<ListboxSelect>>", self.on_hotel_select)
        hotels = self.controller.hotels
        if not hotels:
            self.controller.add_predefined_hotels()
            if not hotels:
                self.hotel_listbox.insert(tk.END, "Немає доступних готелів")
        for hotel in hotels:
            self.hotel_listbox.insert(tk.END, f"{hotel.name}")

        self.search_bar = tk.Entry(self.main_frame, width=13)
        self.search_bar.place(x=300, y=13)
        self.search_button = tk.Button(self.main_frame, text="Шукати")
        self.search_button.place(x=385, y=10)
        self.search_button.bind("<Button-1>", self.search_hotel_by_words)

        self.information_of_hotels = tk.Label(self.main_frame, text="Додаткова інформація:", font=("Arial", 14))
        self.information_of_hotels.pack()
        self.hotel_info_label = tk.Label(self.main_frame, text="\n\n\n\n")
        self.hotel_info_label.pack()

        if client.is_admin:
            self.exit_button = tk.Button(self.main_frame, text="Додати готель", command=self.add_hotel_gui,
                                         font=("Arial", 14))
            self.exit_button.pack(anchor=tk.NE)
            self.exit_button = tk.Button(self.main_frame, text="Видалити готель", command=self.delete_hotel_gui,
                                         font=("Arial", 14))
            self.exit_button.pack(anchor=tk.NE)
        self.back_button = tk.Button(self.main_frame, text="Повернутись назад",
                                     font=("Arial", 14))
        self.back_button.pack(anchor=tk.NE)
        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(anchor=tk.NE)

    def delete_hotel_gui(self):
        index = self.hotel_listbox.curselection()[0]
        name = self.hotel_listbox.get(index)
        self.controller.remove_hotel(name)
        self.hotel_listbox.delete(0, tk.END)
        for hotel in self.controller.hotels:
            self.hotel_listbox.insert(tk.END, hotel.name)

    def add_hotel_gui(self):
        add_hotel_window = tk.Toplevel(self.root)
        add_hotel_window.title("Додати готель")
        add_hotel_window.geometry("300x500")

        tk.Label(add_hotel_window, text="Назва:", font=("Arial", 14)).pack()
        self.name_entry = tk.Entry(add_hotel_window, font=("Arial", 14))
        self.name_entry.pack()

        tk.Label(add_hotel_window, text="Опис:", font=("Arial", 14)).pack()
        self.description_entry = tk.Entry(add_hotel_window, font=("Arial", 14))
        self.description_entry.pack()

        tk.Label(add_hotel_window, text="Кількість кімнат:", font=("Arial", 14)).pack()
        self.total_room_entry = tk.Entry(add_hotel_window, font=("Arial", 14))
        self.total_room_entry.pack()

        tk.Label(add_hotel_window, text="Вартість кімнати:", font=("Arial", 14)).pack()
        self.cost_room_entry = tk.Entry(add_hotel_window, font=("Arial", 14))
        self.cost_room_entry.pack()

        self.button_add_hotel = tk.Button(add_hotel_window, text="Додати", font=("Arial", 14))
        self.button_add_hotel.pack()
        self.button_add_hotel.bind("<Button-1>", self.add_hotel_gui2)

        self.back_button = tk.Button(add_hotel_window, text="Повернутись назад", command=add_hotel_window.destroy,
                                     font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(add_hotel_window, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)

    def add_hotel_gui2(self, event):
        name = self.name_entry.get()
        description = self.description_entry.get()
        total_rooms = int(self.total_room_entry.get())  # Convert to int
        cost_room = float(self.cost_room_entry.get())  # Convert to float
        self.controller.add_hotel(name, description, total_rooms, cost_room)
        self.hotel_listbox.insert(tk.END, name)

    def on_hotel_select(self, event):
        selected_index = self.hotel_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_hotel_name = self.hotel_listbox.get(selected_index)
            hotel = self.controller.find_hotel_by_name(selected_hotel_name)
            if hotel:
                self.hotel_info_label.config(
                    text=f"Назва: {hotel.name}\nОпис: {hotel.description}\nВсього кімнат: {hotel.total_rooms}\n"
                         f"Вільні кімнати: {hotel.available_rooms}\n Вартість номера за 1 ніч: {hotel.cost_of_rooms}")

    def search_hotel_by_words(self, event):
        word = self.search_bar.get()
        self.hotel_listbox.delete(0, tk.END)
        for hotel in self.controller.hotels:
            if word in hotel.name:
                self.hotel_listbox.insert(tk.END, hotel.name)

    def show_booking_form(self, client):
        self.clear_frame()
        tk.Label(self.main_frame, text="Виберіть готель:", font=("Arial", 14)).pack()

        self.hotel_var = tk.StringVar(self.main_frame)
        hotel_names = [hotel.name for hotel in self.controller.hotels]
        self.hotel_var.set(hotel_names[0])
        tk.OptionMenu(self.main_frame, self.hotel_var, *hotel_names).pack()

        tk.Label(self.main_frame, text="Дата заїзду (YYYY-MM-DD):", font=("Arial", 14)).pack()
        self.start_date_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.start_date_entry.pack()

        tk.Label(self.main_frame, text="Дата виїзду (YYYY-MM-DD):", font=("Arial", 14)).pack()
        self.end_date_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.end_date_entry.pack()

        tk.Label(self.main_frame, text="Опис до броні:", font=("Arial", 14)).pack()
        self.booking_text_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.booking_text_entry.pack()

        tk.Button(self.main_frame, text="Забронювати", command=lambda: self.submit_booking(client), font=("Arial", 14)).pack()
        self.back_button = tk.Button(self.main_frame, text="Повернутись назад",
                                     command=lambda: self.go_to_user_menu(client), font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)


    def submit_booking(self, client):
        selected_hotel_name = self.hotel_var.get()
        hotel = self.controller.find_hotel_by_name(selected_hotel_name)

        start_date_str = self.start_date_entry.get()[0:11]
        end_date_str = self.end_date_entry.get()[0:11]

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Непрвильний формат. Будь ласка, використовуйте формат: YYYY-MM-DD.")
            return

        booking_text = self.booking_text_entry.get()

        if start_date >= end_date:
            messagebox.showerror("Error", "Дата виїзду має йти після дати заїзду.")
            return

        if hotel.available_rooms == 0:
            messagebox.showerror("Error", "Наразі немає вільних кімнат.")
            return

        self.controller.add_booking(client, hotel, start_date, end_date, booking_text)
        messagebox.showinfo("Бронь", "Бронь підтверджена")
        self.show_user_menu(client)


    def view_client_bookings(self, client):
        self.clear_frame()
        tk.Label(self.main_frame, text="Ваші броні:", font=("Arial", 14)).pack()

        bookings = client.bookings
        if not bookings:
            tk.Label(self.main_frame, text="У вас немає заброньованих номерів.", font=("Arial", 14)).pack()
        else:
            self.booking_listbox = tk.Listbox(self.main_frame, width=100)
            self.booking_listbox.pack(fill=tk.BOTH, expand=1)
            for booking in bookings:
                self.booking_listbox.insert(tk.END,
                                            f"Готель: {booking.hotel.name}, Дата заїзду: {str(booking.start_date)[0:11]}, Дата виїзду: {str(booking.end_date)[0:11]}\n, Опис: {booking.text}")

            tk.Button(self.main_frame, text="Змінити бронь", command=self.edit_booking, font=("Arial", 14)).pack(pady=10)
            tk.Button(self.main_frame, text="Видалити бронь", command=self.delete_booking, font=("Arial", 14)).pack()

        self.back_button = tk.Button(self.main_frame, text="Повернутись назад", command=lambda: self.go_to_user_menu(client),
                                     font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(self.main_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)


    def edit_booking(self):
        selected_index = self.booking_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_booking_text = self.booking_listbox.get(selected_index)
            # Extracting hotel name, start date, end date, and booking text from the selected booking text
            parts = selected_booking_text.split(", ")
            hotel_name = parts[0].split(": ")[1]
            start_date_str = parts[1].split(": ")[1]
            end_date_str = parts[2].split(": ")[1]
            booking_text = parts[3].split(": ")[1]

            # Create a new window for editing booking
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Зміна броні")
            edit_window.geometry("300x300")

            # Entry fields to edit booking information
            tk.Label(edit_window, text="Назва готелю:").grid(row=0, column=0)
            hotel_var = tk.StringVar(edit_window, value=hotel_name)
            tk.Entry(edit_window, textvariable=hotel_var, state="readonly").grid(row=0, column=1)

            tk.Label(edit_window, text="Дата заселення (YYYY-MM-DD):").grid(row=1, column=0)
            start_date_var = tk.StringVar(edit_window, value=start_date_str)
            tk.Entry(edit_window, textvariable=start_date_var).grid(row=1, column=1)

            tk.Label(edit_window, text="Дата виїзду (YYYY-MM-DD):").grid(row=2, column=0)
            end_date_var = tk.StringVar(edit_window, value=end_date_str)
            tk.Entry(edit_window, textvariable=end_date_var).grid(row=2, column=1)

            tk.Label(edit_window, text="Опис:").grid(row=3, column=0)
            booking_text_var = tk.StringVar(edit_window, value=booking_text)
            tk.Entry(edit_window, textvariable=booking_text_var).grid(row=3, column=1)

            # Submit button to save the changes
            tk.Button(edit_window, text="Зберегти зміни", command=lambda: self.save_booking_changes(
                selected_index, hotel_var.get(), start_date_var.get(), end_date_var.get(), booking_text_var.get())).grid(
                row=4, column=0, columnspan=2)

            self.back_button = tk.Button(edit_window, text="Повернутись назад", command=edit_window.destroy,
                                         font=("Arial", 14))
            self.back_button.grid(row=5, column=0, pady=5)
            self.exit_button = tk.Button(edit_window, text="Вийти", command=self.exit, font=("Arial", 14))
            self.exit_button.grid(row=5, column=1, pady=5)


    def save_booking_changes(self, index, hotel_name, start_date, end_date, booking_text):
        # Update the booking in the client's bookings list
        client = self.controller.logged_in_client
        client.bookings[
            index] = f"Готель: {hotel_name}, Дата заїзду: {start_date}, Дата виїзду: {end_date}, Опис: {booking_text}"
        # Update the listbox
        self.booking_listbox.delete(index)
        self.booking_listbox.insert(index, client.bookings[index])


    def delete_booking(self):
        selected_index = self.booking_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            # Delete the booking from the client's bookings list
            client = self.controller.logged_in_client
            del client.bookings[index]
            # Update the listbox
            self.booking_listbox.delete(index)


    def user_list_window(self, event):
        self.clear_frame()
        self.user_list_frame = tk.Frame(self.main_frame)
        self.user_list_frame.pack()
        self.search_bar_client = tk.Entry(self.user_list_frame, width=13)
        self.search_bar_client.pack(anchor=tk.NE)
        self.search_button_client = tk.Button(self.user_list_frame, text="Шукати")
        self.search_button_client.pack(anchor=tk.NE)
        self.search_button_client.bind("<Button-1>", self.search_client_by_words)

        self.user_listbox = tk.Listbox(self.user_list_frame, width=100)
        self.user_listbox.pack(pady=10)
        self.update_user_listbox()

        tk.Button(self.user_list_frame, text="Додати клієнта", command=self.add_client_window, font=("Arial", 14)).pack(
            pady=5)
        tk.Button(self.user_list_frame, text="Видалити клієнта", command=self.delete_client, font=("Arial", 14)).pack(
            pady=5)
        tk.Button(self.user_list_frame, text="Змінити дані клієнта", command=self.edit_client_window,
                  font=("Arial", 14)).pack(pady=5)
        tk.Button(self.user_list_frame, text="Переглянути дані клієнта", command=self.view_client_details,
                  font=("Arial", 14)).pack(pady=5)
        tk.Button(self.user_list_frame, text="Сортувати за ім'ям", command=lambda: self.sort_clients('first_name'),
                  font=("Arial", 14)).pack(pady=5)
        tk.Button(self.user_list_frame, text="Сортувати за прізвищем", command=lambda: self.sort_clients('last_name'),
                  font=("Arial", 14)).pack(pady=5)
        self.back_button = tk.Button(self.user_list_frame, text="Повернутись назад", command=self.go_back_to_widgets,
                                     font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(self.user_list_frame, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)

    def search_client_by_words(self, event):
        word = self.search_bar_client.get()
        self.user_listbox.delete(0, tk.END)
        for client in self.controller.clients:
            if word in client.first_name or word in client.last_name:
                self.user_listbox.insert(tk.END, f"{client.first_name} {client.last_name} ({client.email})")

    def update_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        for client in self.controller.clients:
            self.user_listbox.insert(tk.END, f"{client.first_name} {client.last_name} ({client.email})")

    def add_client_window(self):
        add_client_window = tk.Toplevel(self.root)
        add_client_window.title("Додати клієнта")
        add_client_window.geometry("300x300")

        tk.Label(add_client_window, text="Ім'я:", font=("Arial", 14)).pack()
        first_name_entry = tk.Entry(add_client_window, font=("Arial", 14))
        first_name_entry.pack()

        tk.Label(add_client_window, text="Прізвище:", font=("Arial", 14)).pack()
        last_name_entry = tk.Entry(add_client_window, font=("Arial", 14))
        last_name_entry.pack()

        tk.Label(add_client_window, text="Email:", font=("Arial", 14)).pack()
        email_entry = tk.Entry(add_client_window, font=("Arial", 14))
        email_entry.pack()

        tk.Label(add_client_window, text="Пароль:", font=("Arial", 14)).pack()
        password_entry = tk.Entry(add_client_window, font=("Arial", 14))
        password_entry.pack()

        admin_var = tk.BooleanVar()
        admin_checkbutton = tk.Checkbutton(add_client_window, text="Я адмін", variable=admin_var, font=("Arial", 14))
        admin_checkbutton.pack()

        def add_client():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            is_admin = admin_var.get()
            self.controller.add_client(first_name, last_name, email, password, is_admin)
            messagebox.showinfo("Додати клієнта", "Клієнта додано успішно!")
            add_client_window.destroy()
            self.update_user_listbox()

        tk.Button(add_client_window, text="Додати", command=add_client, font=("Arial", 14)).pack(pady=10)
        self.back_button = tk.Button(add_client_window, text="Повернутись назад", command=add_client_window.destroy,
                                     font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(add_client_window, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)

    def delete_client(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Видалити клієнта", "Виберіть клієнта для видалення")
            return
        client_str = self.user_listbox.get(selected_index)
        email = client_str.split('(')[1][:-1]  # Extract the email from the string
        self.controller.remove_client(email)
        messagebox.showinfo("Видалити клієнта", "Клієнта видалено успішно!")
        self.update_user_listbox()

    def edit_client_window(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Змінити дані клієнта", "Виберіть клієнта для редагування")
            return
        client_str = self.user_listbox.get(selected_index)
        email = client_str.split('(')[1][:-1]  # Extract the email from the string
        client = self.controller.find_client_by_email(email)
        if not client:
            messagebox.showerror("Змінити дані клієнта", "Клієнта не знайдено")
            return

        edit_client_window = tk.Toplevel(self.root)
        edit_client_window.title("Змінити дані клієнта")
        edit_client_window.geometry("300x300")

        tk.Label(edit_client_window, text="Ім'я:", font=("Arial", 14)).pack()
        first_name_entry = tk.Entry(edit_client_window, font=("Arial", 14))
        first_name_entry.insert(0, client.first_name)
        first_name_entry.pack()

        tk.Label(edit_client_window, text="Прізвище:", font=("Arial", 14)).pack()
        last_name_entry = tk.Entry(edit_client_window, font=("Arial", 14))
        last_name_entry.insert(0, client.last_name)
        last_name_entry.pack()
        tk.Label(edit_client_window, text="Email:", font=("Arial", 14)).pack()
        email_entry = tk.Entry(edit_client_window, font=("Arial", 14))
        email_entry.insert(0, client.email)
        email_entry.pack()

        tk.Label(edit_client_window, text="Пароль:", font=("Arial", 14)).pack()
        password_entry = tk.Entry(edit_client_window, font=("Arial", 14))
        password_entry.insert(0, client.password)
        password_entry.pack()

        admin_var = tk.BooleanVar()
        admin_checkbutton = tk.Checkbutton(edit_client_window, text="Я адмін", variable=admin_var, font=("Arial", 14))
        admin_checkbutton.pack()
        if client.is_admin:
            admin_checkbutton.select()

        def edit_client():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            is_admin = admin_var.get()
            self.controller.edit_client(client.email, first_name, last_name, email, password, is_admin)
            messagebox.showinfo("Змінити дані клієнта", "Дані клієнта змінено успішно!")
            edit_client_window.destroy()
            self.update_user_listbox()

        tk.Button(edit_client_window, text="Змінити", command=edit_client, font=("Arial", 14)).pack(pady=10)
        self.back_button = tk.Button(edit_client_window, text="Повернутись назад", command=edit_client_window.destroy,
                                     font=("Arial", 14))
        self.back_button.pack(pady=5)
        self.exit_button = tk.Button(edit_client_window, text="Вийти", command=self.exit, font=("Arial", 14))
        self.exit_button.pack(pady=5)

    def view_client_details(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Переглянути дані клієнта", "Виберіть клієнта для перегляду")
            return
        client_str = self.user_listbox.get(selected_index)
        email = client_str.split('(')[1][:-1]  # Extract the email from the string
        client = self.controller.find_client_by_email(email)
        if not client:
            messagebox.showerror("Переглянути дані клієнта", "Клієнта не знайдено")
            return

        details = f"Ім'я: {client.first_name}\nПрізвище: {client.last_name}\nEmail: {client.email}\nАдмін: {'Так' if client.is_admin else 'Ні'}"
        messagebox.showinfo("Дані клієнта", details)

    def sort_clients(self, by):
        self.controller.sort_clients(by)
        self.update_user_listbox()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()




if __name__ == "__main__":
    from controller import HotelController

    root = tk.Tk()
    controller = HotelController()
    app = HotelBookingApp(root, controller)
    root.geometry("500x515")
    root.mainloop()

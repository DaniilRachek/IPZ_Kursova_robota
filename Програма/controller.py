import pickle
import os
from main import Hotel, Client, Booking


class HotelController: # клас, який відображає controller з функціями управління у програмі
    def __init__(self):
        self.hotels = []
        self.clients = []
        self.load_data()
        self.logged_in_client = None

    def add_hotel(self, name, description, total_rooms, cost_of_rooms): # функція для додавання готелю
        hotel = Hotel(name, description, total_rooms, cost_of_rooms=cost_of_rooms)
        self.hotels.append(hotel)
        self.save_data()
        return hotel

    def add_client(self, first_name, last_name, email, password, is_admin):  # функція для додавання користувача
        client = Client(first_name, last_name, email, password, is_admin)
        self.clients.append(client)
        self.save_data()
        return client

    def remove_client(self, email):  # функція для видалення користувача
        for client in self.clients:
            if client.email == email:
                self.clients.remove(client)
            self.save_data()

    def edit_client(self, email, name, surname, new_email, password, is_admin):  # функція для зміни даних користувача
        for client in self.clients:
            if client.email == email:
                client.first_name = name
                client.last_name = surname
                client.email = new_email
                client.password = password
                client.is_admin = is_admin
            self.save_data()

    def sort_clients(self, by):  # функція для сортування користувачів
        if by == "first_name":
            self.clients.sort(key=lambda client: client.first_name)
        elif by == "last_name":
            self.clients.sort(key=lambda client: client.last_name)

    def find_hotel_by_name(self, name):  # функція для пошуку готелів за назвою
        for hotel in self.hotels:
            if hotel.name == name:
                return hotel
        return None

    def find_client_by_email(self, email):  # функція для пошуку користувачів за emailoм
        for client in self.clients:
            if client.email == email:
                return client
        return None

    def add_booking(self, client, hotel, start_date, end_date, text): # функція для додавання броні
        booking = Booking(client, hotel, start_date, end_date, text)
        hotel.add_booking(booking)
        client.add_booking(booking)
        self.save_data()

    def remove_booking(self, client, hotel, booking): # функція для видалення броні
        hotel.remove_booking(booking)
        client.remove_booking(booking)
        self.save_data()

    def save_data(self): # функція для збереження даних для подальшого використання
        with open('data.pkl', 'wb') as file:
            pickle.dump({'hotels': self.hotels, 'clients': self.clients}, file)

    def load_data(self): # функція для завантаження даних
        if os.path.exists('data.pkl'):
            with open('data.pkl', 'rb') as file:
                data = pickle.load(file)
                self.hotels = data['hotels']
                self.clients = data['clients']
        else:
            self.add_predefined_hotels()

    def add_predefined_hotels(self): # функція для додання початкових готелів
        self.add_hotel("Готель Київ", "Комфортабельні номери обладнані всім необхідним для відпочинку.", 20, 450)
        self.add_hotel("Готель Львів", "Ідеальний вибір для тих, хто цінує комфорт та високий рівень сервісу.", 30, 600)
        self.add_hotel("Готель Одеса", "Тут ви знайдете просторі номери, дитячий майданчик, ресторан з домашньою кухнею.", 10, 200)
        self.save_data()

    def remove_hotel(self, name): # функція для видалення готелів
        if self.logged_in_client and self.logged_in_client.is_admin:
            for hotel in self.hotels:
                if hotel.name == name:
                    self.hotels.remove(hotel)
                    self.save_data()
        else:
            print("You don't have permission to perform this action.")
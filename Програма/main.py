class Hotel:  # клас для відображення готелів та їх характеристик
    def __init__(self, name, description, total_rooms, cost_of_rooms):
        self.name = name
        self.description = description
        self.total_rooms = total_rooms
        self.cost_of_rooms = cost_of_rooms
        self.available_rooms = total_rooms
        self.bookings = []

    def add_booking(self, booking):  # функція для додавання броні в готелі
        if self.available_rooms > 0:
            self.bookings.append(booking)
            self.available_rooms -= 1

    def remove_booking(self, booking):   # функція для видалення броні в готелі
        if booking in self.bookings:
            self.bookings.remove(booking)
            self.available_rooms += 1


class Client: # клас для відображення користувачів, та їх характеристик
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.bookings = []

    def add_booking(self, booking): # Функція для додавання броні користувачу
        self.bookings.append(booking)

    def remove_booking(self, booking): # Функція для видалення броні у користувача
        if booking in self.bookings:
            self.bookings.remove(booking)


class Booking: # Клас, який відображає броні
    def __init__(self, client, hotel, start_date, end_date, text):
        self.client = client
        self.hotel = hotel
        self.start_date = start_date
        self.end_date = end_date
        self.text = text

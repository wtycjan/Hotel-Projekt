import database
import system
from reservations import Reservation
from hotel import Hotel
from system import System


class Guest:
    reservations = Reservation()
    hotels = Hotel()
    system = System()

    def client_menu(self, user_id):
        user_input = input(system.CLIENT_MENU)
        while True:
            if user_input == 'hotels':
                self.hotels.list_hotels()
            elif user_input == 'more':
                self.hotels.hotel_info()
            elif user_input == 'res':
                self.reservations.make_reservation(user_id)
            elif user_input == 'my res':
                self.client_reservations_menu(user_id)
            elif user_input == 'log out':
                self.system.menu()
            else:
                print("Unknown command! try again.")

            user_input = input(system.CLIENT_MENU)

    def client_reservations_menu(self, user_id):
        user_input = input(system.CLIENT_RESERVATIONS_MENU)
        while user_input != 'back':
            if user_input == 'list res':
                self.list_my_reservations_info(user_id)
            elif user_input == 'edit':
                self.reservations.pick_to_edit_my_reservation_menu(user_id)
            elif user_input == 'del':
                self.reservations.pick_to_delete_my_reservation_menu(user_id)
            else:
                print("Unknown command! try again.")

            user_input = input(system.CLIENT_RESERVATIONS_MENU)

    @staticmethod
    def list_all_reservations():
        reservation_list = database.get_all_reservations_info()
        for reservation in reservation_list:
            print(f"Reservation number: {reservation['reservation_ID']}\n"
                  f"\tClient: {reservation['user_name']} {reservation['user_surname']}\n"
                  f"\tHotel: {reservation['hotel_name']}\n"
                  f"\tDate: {reservation['first_day']} - {reservation['last_day']}\n"
                  f"\tRoom: {reservation['room_ID']} {reservation['room_type']}\n"
                  f"\tDining option: {reservation['dining_option_type']}\n"
                  f"\tPayment: {reservation['payment_method']} - {reservation['cost']} PLN")

    @staticmethod
    def list_my_reservations_info(user_id):
        reservation_list = database.get_my_reservations_info(user_id)
        for reservation in reservation_list:
            print(f"Reservation number: {reservation['reservation_ID']}\n"
                  f"\tClient: {reservation['user_name']} {reservation['user_surname']}\n"
                  f"\tHotel: {reservation['hotel_name']}\n"
                  f"\tDate: {reservation['first_day']} - {reservation['last_day']}\n"
                  f"\tRoom: {reservation['room_ID']} {reservation['room_type']}\n"
                  f"\tDining option: {reservation['dining_option_type']}\n"
                  f"\tPayment: {reservation['payment_method']} - {reservation['cost']} PLN")

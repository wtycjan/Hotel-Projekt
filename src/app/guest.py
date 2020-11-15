import database
import system
from reservations import Reservation
from hotel import Hotel


class Guest:
    reservations = Reservation()
    hotels = Hotel()

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
                system.System().menu()
            else:
                print("Unknown command! try again.")

            user_input = input(system.CLIENT_MENU)

    def client_reservations_menu(self, user_id):
        user_input = input(system.CLIENT_RESERVATIONS_MENU)
        while user_input != 'back':
            if user_input == 'list res':
                self.reservations.list_my_reservations_info(user_id)
            elif user_input == 'edit':
                self.reservations.pick_to_edit_my_reservation_menu(user_id)
            elif user_input == 'del':
                self.reservations.pick_to_delete_my_reservation_menu(user_id)
            else:
                print("Unknown command! try again.")

            user_input = input(system.CLIENT_RESERVATIONS_MENU)



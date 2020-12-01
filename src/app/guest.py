from database import Database
import system
from reservations import Reservation
from hotel import Hotel


class Guest:
    reservations = Reservation()
    hotels = Hotel()
    database = Database()

    def client_menu(self, user_id):
        user_input = input(system.CLIENT_MENU)
        print(self.database)
        while True:
            if user_input == 'hotels':
                self.hotels.list_hotels()
            elif user_input == 'more':
                self.hotels.hotel_info()
            elif user_input == 'res':
                self.make_reservation(user_id)
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
                self.pick_to_edit_my_reservation_menu(user_id)
            elif user_input == 'del':
                self.pick_to_delete_my_reservation_menu(user_id)
            else:
                print("Unknown command! try again.")

            user_input = input(system.CLIENT_RESERVATIONS_MENU)


    def make_reservation(self, user_id):
        user_input = input(system.RESERVATION_MENU_INTERFACE)
        while user_input != 'back':
            if user_input == 'fill':
                print("Here is the reservation form:")
                hotel_id = self.hotels.choose_hotel()

                date_format = '%Y-%m-%d'
                first_day_obj = self.reservations.choose_start_date(date_format)

                last_day_obj = self.reservations.choose_end_date(date_format, first_day_obj)

                reservation_period = last_day_obj - first_day_obj

                room_id, room_cost = self.reservations.choose_room(hotel_id)

                dining_option_id, dining_option_cost = self.reservations.choose_dining_option()

                payment_method_id, payment_method_discount = self.reservations.choose_payment_method()

                reservation_cost = round(
                    self.reservations.calculate_cost(reservation_period.days, room_cost, dining_option_cost,
                                        payment_method_discount), 2)
                print(f"Reservation cost: {reservation_cost} PLN for {reservation_period.days} days.")

                decision = input(system.DECISION_INTERFACE)
                while True:
                    if decision == 'save':
                        self.database.add_reservation(user_id, hotel_id, first_day_obj.date(), last_day_obj.date(), room_id,
                                                 dining_option_id, payment_method_id, reservation_cost)
                        print("Your reservation has been saved.")
                        break
                    elif decision == 'cancel':
                        print("You have discarded your reservation.")
                        break
                    else:
                        print("Unknown command! Try again.")
                    decision = input(system.DECISION_INTERFACE)
            else:
                print("Unknown command! Try again.")

            user_input = input(system.RESERVATION_MENU_INTERFACE)

    def pick_to_edit_my_reservation_menu(self, user_id):
        user_input = input(system.CLIENT_PICK_TO_EDIT_RESERVATION_MENU)
        while user_input != 'back':
            if user_input == 'pick':
                reservation_obj = self.reservations.choose_reservation(user_id, 'edit')
                self.edit_my_reservation(reservation_obj[0])
            else:
                print("Unknown command! Try again.")

            user_input = input(system.CLIENT_PICK_TO_EDIT_RESERVATION_MENU)

    def edit_my_reservation(self, reservation_obj):
        user_input = input(system.CLIENT_EDIT_RESERVATION_MENU)
        while True:
            if user_input == 'hotel':
                reservation_obj['hotel_id'] = self.hotels.choose_hotel()

            elif user_input == 'date':
                date_format = '%Y-%m-%d'
                reservation_obj['first_day'] = self.reservations.choose_start_date(date_format)
                reservation_obj['last_day'] = self.reservations.choose_end_date(date_format, reservation_obj['first_day'])

            elif user_input == 'room':
                reservation_obj['room_id'], reservation_obj['room_type_price'] = self.reservations.choose_room(
                    reservation_obj['hotel_id'])

            elif user_input == 'dining':
                reservation_obj['dining_option_id'], reservation_obj['dining_option_cost'] = self.reservations.choose_dining_option()

            elif user_input == 'payment':
                reservation_obj['payment_method_id'], reservation_obj[
                    'payment_method_discount'] = self.reservations.choose_payment_method()

            elif user_input == 'save':
                reservation_period = reservation_obj['last_day'] - reservation_obj['first_day']
                reservation_obj['cost'] = round(
                    self.reservations.calculate_cost(reservation_period.days, reservation_obj['room_type_price'],
                                   reservation_obj['dining_option_cost'],
                                   reservation_obj['payment_method_discount']), 2)
                print(f"Reservation cost: {reservation_obj['cost']} PLN for {reservation_period.days} days.")
                decision = input(system.EDIT_DECISION_INTERFACE)
                if decision == 'yes':
                    self.database.update_my_reservation(reservation_obj['hotel_id'], reservation_obj['first_day'],
                                                   reservation_obj['last_day'], reservation_obj['room_id'],
                                                   reservation_obj['dining_option_id'],
                                                   reservation_obj['payment_method_id'], reservation_obj['cost'],
                                                   reservation_obj['reservation_ID'])
                    break
                elif decision == 'no':
                    pass
                else:
                    print("Unknown command! Try again.")

            elif user_input == 'cancel':
                break
            else:
                print("Unknown command! Try again.")

            user_input = input(system.CLIENT_EDIT_RESERVATION_MENU)

    def pick_to_delete_my_reservation_menu(self, user_id):
        user_input = input(system.CLIENT_PICK_TO_DELETE_RESERVATION_MENU)
        while user_input != 'back':
            if user_input == 'pick':
                reservation_obj = self.reservations.choose_reservation(user_id, 'delete')
                decision = input(system.DELETE_DECISION_INTERFACE)
                if decision == 'yes':
                    self.database.delete_reservation(reservation_obj[0]['reservation_ID'])
                    print("Your reservation has been deleted.")
                elif decision == 'no':
                    pass
                else:
                    print("Unknown command! Try again.")
            elif user_input == 'delete all':
                decision = input(system.DELETE_DECISION_INTERFACE)
                if decision == 'yes':
                    self.database.delete_all_my_reservation(user_id)
                    print("All your reservations have been deleted.")
                    break
                elif decision == 'no':
                    pass
                else:
                    print("Unknown command! Try again.")
            else:
                print("Unknown command! Try again.")

            user_input = input(system.CLIENT_PICK_TO_DELETE_RESERVATION_MENU)


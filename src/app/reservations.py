from datetime import datetime

import system
import database
from hotel import Hotel
from guest import Guest

class Reservation:
    hotels = Hotel()
    guest = Guest()

    def make_reservation(self, user_id):
        user_input = input(system.RESERVATION_MENU_INTERFACE)
        while user_input != 'back':
            if user_input == 'fill':
                print("Here is the reservation form:")
                hotel_id = self.choose_hotel()

                date_format = '%Y-%m-%d'
                first_day_obj = self.choose_start_date(date_format)

                last_day_obj = self.choose_end_date(date_format, first_day_obj)

                reservation_period = last_day_obj - first_day_obj

                room_id, room_cost = self.choose_room(hotel_id)

                dining_option_id, dining_option_cost = self.choose_dining_option()

                payment_method_id, payment_method_discount = self.choose_payment_method()

                reservation_cost = round(
                    self.calculate_cost(reservation_period.days, room_cost, dining_option_cost,
                                        payment_method_discount), 2)
                print(f"Reservation cost: {reservation_cost} PLN for {reservation_period.days} days.")

                decision = input(system.DECISION_INTERFACE)
                while True:
                    if decision == 'save':
                        database.add_reservation(user_id, hotel_id, first_day_obj.date(), last_day_obj.date(), room_id,
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
                reservation_obj = self.choose_reservation(user_id, 'edit')
                self.edit_my_reservation(reservation_obj[0])
            else:
                print("Unknown command! Try again.")

            user_input = input(system.CLIENT_PICK_TO_EDIT_RESERVATION_MENU)

    def edit_my_reservation(self, reservation_obj):
        user_input = input(system.CLIENT_EDIT_RESERVATION_MENU)
        while True:
            if user_input == 'hotel':
                reservation_obj['hotel_id'] = self.choose_hotel()

            elif user_input == 'date':
                date_format = '%Y-%m-%d'
                reservation_obj['first_day'] = self.choose_start_date(date_format)
                reservation_obj['last_day'] = self.choose_end_date(date_format, reservation_obj['first_day'])

            elif user_input == 'room':
                reservation_obj['room_id'], reservation_obj['room_type_price'] = self.choose_room(
                    reservation_obj['hotel_id'])

            elif user_input == 'dining':
                reservation_obj['dining_option_id'], reservation_obj['dining_option_cost'] = self.choose_dining_option()

            elif user_input == 'payment':
                reservation_obj['payment_method_id'], reservation_obj[
                    'payment_method_discount'] = self.choose_payment_method()

            elif user_input == 'save':
                reservation_period = reservation_obj['last_day'] - reservation_obj['first_day']
                reservation_obj['cost'] = round(
                    self.calculate_cost(reservation_period.days, reservation_obj['room_type_price'],
                                   reservation_obj['dining_option_cost'],
                                   reservation_obj['payment_method_discount']), 2)
                print(f"Reservation cost: {reservation_obj['cost']} PLN for {reservation_period.days} days.")
                decision = input(system.EDIT_DECISION_INTERFACE)
                if decision == 'yes':
                    database.update_my_reservation(reservation_obj['hotel_id'], reservation_obj['first_day'],
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

    def calculate_cost(self, reservation_period, room_cost, dining_option_cost, payment_method_discount):
        return (reservation_period * room_cost + dining_option_cost) * payment_method_discount

    def check_date_format(self, date_string, date_format):
        while True:
            try:
                datetime.datetime.strptime(date_string, date_format)
                print("This is the correct date format.")
            except ValueError:
                date_string = input("This is the incorrect date format. It should be YYYY-MM-DD: ")
                continue
            else:
                break
        return datetime.datetime.strptime(date_string, date_format), date_string

    def choose_hotel(self):
        self.hotels.list_hotels()
        hotel_id = int(input("Enter the number of hotel from list above: "))
        hotels = database.get_all_hotels()
        searching = True
        while searching:
            for hotel in hotels:
                if hotel['hotel_ID'] == hotel_id:
                    searching = False
                    break
            if searching:
                self.hotels.list_hotels()
                hotel_id = int(input("Enter the proper hotel number from list above: "))
        return hotel_id

    def choose_start_date(self, date_format):
        first_day = input("Enter first day of your reservation 'RRRR-MM-DD': ")
        first_day_obj, first_day = self.check_date_format(first_day, date_format)
        while True:
            if first_day_obj < datetime.datetime.now():
                first_day = input("The reservation may start at the earliest today 'RRRR-MM-DD': ")
                first_day_obj, first_day = self.check_date_format(first_day, date_format)
            else:
                break
        return first_day_obj

    def choose_end_date(self, date_format, first_day_obj):
        last_day = input("Enter the last day of your reservation 'RRRR-MM-DD': ")
        last_day_obj, last_day = self.check_date_format(last_day, date_format)
        while True:
            if last_day_obj < first_day_obj:
                last_day = input("Reservation can not end before the first day 'RRRR-MM-DD': ")
                last_day_obj, last_day = self.check_date_format(last_day, date_format)
            else:
                break
        return last_day_obj

    def choose_room(self, hotel_id):
        self.hotels.list_all_rooms(hotel_id)
        room_id = int(input("Enter the room number from a list above you want to book: "))
        rooms = database.get_all_rooms(hotel_id)
        room_cost = 0
        searching = True
        while searching:
            for room in rooms:
                if room['room_ID'] == room_id:
                    searching = False
                    room_cost = room['room_type_price']
                    break
            if searching:
                self.hotels.list_all_rooms(hotel_id)
                room_id = int(input("Enter the proper room number from a list above you want to book: "))
        return room_id, room_cost

    def choose_dining_option(self):
        self.hotels.list_dining_options()
        dining_option_id = int(input("Enter dining option number from a list above: "))
        dining_options = database.get_dining_options()
        dining_option_cost = 0
        searching = True
        while searching:
            for dining_option in dining_options:
                if dining_option['dining_option_ID'] == dining_option_id:
                    searching = False
                    dining_option_cost = dining_option['dining_option_cost']
                    break
            if searching:
                self.hotels.list_dining_options()
                dining_option_id = int(input("Enter proper dining option number from a list above: "))
        return dining_option_id, dining_option_cost

    def choose_payment_method(self):
        self.hotels.list_payment_methods()
        payment_method_id = int(input("Enter payment method number from a list above: "))
        payment_methods = database.get_payment_methods()
        payment_method_discount = 0
        searching = True
        while searching:
            for payment_method in payment_methods:
                if payment_method['payment_method_ID'] == payment_method_id:
                    searching = False
                    payment_method_discount = payment_method['payment_method_discount']
                    break
            if searching:
                self.hotels.list_payment_methods()
                payment_method_id = int(input("Enter proper payment method number from a list above: "))
        return payment_method_id, payment_method_discount

    def choose_reservation(self, user_id, action_name):
        self.guest.list_my_reservations_info(user_id)
        reservation_id = int(input(f"Enter the reservation number from a list above, you want to {action_name}: "))
        reservations = database.get_my_reservations_info(user_id)
        searching = True
        reservation_obj = 0
        while searching:
            for reservation in reservations:
                if reservation['reservation_ID'] == reservation_id:
                    reservation_obj = database.get_my_reservation(reservation_id)
                    searching = False
                    break
            if searching:
                self.guest.list_my_reservations_info(user_id)
                reservation_id = int(
                    input(f"Enter the proper reservation number from a list above, you want to {action_name}: "))
        return reservation_obj

    def pick_to_delete_my_reservation_menu(self, user_id):
        user_input = input(system.CLIENT_PICK_TO_DELETE_RESERVATION_MENU)
        while user_input != 'back':
            if user_input == 'pick':
                reservation_obj = self.choose_reservation(user_id, 'delete')
                decision = input(system.DELETE_DECISION_INTERFACE)
                if decision == 'yes':
                    database.delete_reservation(reservation_obj[0]['reservation_ID'])
                    print("Your reservation has been deleted.")
                elif decision == 'no':
                    pass
                else:
                    print("Unknown command! Try again.")
            elif user_input == 'delete all':
                decision = input(system.DELETE_DECISION_INTERFACE)
                if decision == 'yes':
                    database.delete_all_my_reservation(user_id)
                    print("All your reservations have been deleted.")
                    break
                elif decision == 'no':
                    pass
                else:
                    print("Unknown command! Try again.")
            else:
                print("Unknown command! Try again.")

            user_input = input(system.CLIENT_PICK_TO_DELETE_RESERVATION_MENU)

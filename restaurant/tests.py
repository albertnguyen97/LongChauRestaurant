import random
import json
from faker import Faker

fake = Faker()

def generate_booking_data(num_bookings=50):
    bookings = []

    for _ in range(num_bookings):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = fake.phone_number()
        guest_number = random.randint(1, 10)
        comment = fake.text(max_nb_chars=1000)
        reservation_date = fake.date_between(start_date='-30d', end_date='+30d').strftime('%Y-%m-%d')  # Random date within the last 30 days and next 30 days
        reservation_slot = random.randint(11, 19)  # Random slot between 11 and 19

        booking_data = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'guest_number': guest_number,
            'comment': comment,
            'reservation_date': reservation_date,
            'reservation_slot': reservation_slot
        }

        bookings.append(booking_data)

    return bookings


def save_as_json(data, filename='bookings.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    bookings = generate_booking_data()
    save_as_json(bookings)
    print("Booking data saved as bookings.json")

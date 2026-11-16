"""Movie theater ticket booking and seating management."""

import hashlib
import json
import os
import secrets

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat and record the booking."""
    if order_history is None:
        order_history = []

    seat = THEATER_SEATS.get(seat_id)
    if seat is None or seat["is_sold"]:
        return False

    seat["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a reservation for a valid seat."""
    seat = THEATER_SEATS.get(seat_id)
    if seat is None or not seat["is_sold"]:
        return False

    seat["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return whether a seat exists and is available."""
    seat = THEATER_SEATS.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, discount_multiplier):
    """Calculate a ticket price using a multiplier between zero and one."""
    if seat_id not in THEATER_SEATS:
        raise ValueError(f"Unknown seat: {seat_id}")
    if not 0 <= discount_multiplier <= 1:
        raise ValueError("Discount multiplier must be between 0 and 1.")

    base_price = THEATER_SEATS[seat_id]["price"]
    return base_price * discount_multiplier


def generate_ticket_hash(ticket_code):
    """Generate a SHA-256 digest for a ticket code."""
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a cryptographically secure four-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Export the seating chart to a JSON-formatted text file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(THEATER_SEATS, file, indent=4)

    print(f"Seating chart exported to: {filename}")


def get_theater_summary(theater_seats):
    """Return the number of seats currently sold."""
    return sum(
        1 for details in theater_seats.values() if details["is_sold"]
    )


def main():
    """Demonstrate ticket booking system operations."""
    order_history = []

    reserve_seat("A1", "Sarah Connor", order_history)
    cancel_seat("A2")

    print("Is B1 available:", check_seat_status("B1"))
    print(
        "Promo price:",
        compute_discounted_price("B1", 0.80),
    )
    print("Ticket hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())

    export_seating_chart()
    print("Sold count:", get_theater_summary(THEATER_SEATS))

    box_office_key = os.getenv("BOX_OFFICE_KEY")
    print("Box office key configured:", bool(box_office_key))


if __name__ == "__main__":
    main()

import bcrypt
from faker import Faker
from app import app
from models import db, User, BNBListing, Booking
import random
from datetime import datetime, timedelta

fake = Faker()

with app.app_context():

    # --------------------
    # Clear old data
    # --------------------
    db.session.query(Booking).delete()
    db.session.query(BNBListing).delete()
    db.session.query(User).delete()

    db.session.commit()

    print("Database cleared")

    # --------------------
    # Create Users (mix of hosts & clients)
    # --------------------
    users = []

    for i in range(10):
        role = "host" if i < 4 else "client"

        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            phone=fake.unique.phone_number(),
            role=role,
            password_hash=bcrypt.hashpw(
                "password123".encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
        )

        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Users seeded")

    # --------------------
    # Create Listings (only hosts)
    # --------------------
    hosts = [u for u in users if u.role == "host"]

    listings = []

    for host in hosts:
        for _ in range(2):
            listing = BNBListing(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=120),
                location=fake.city(),
                price_per_night=round(random.uniform(20, 200), 2),
                host_id=host.id
            )
            listings.append(listing)

    db.session.add_all(listings)
    db.session.commit()

    print("Listings seeded")

    # --------------------
    # Create Bookings (clients booking listings)
    # --------------------
    clients = [u for u in users if u.role == "client"]

    bookings = []

    for client in clients:
        for _ in range(2):
            listing = random.choice(listings)

            check_in = datetime.now().date() + timedelta(days=random.randint(1, 10))
            check_out = check_in + timedelta(days=random.randint(1, 5))

            nights = (check_out - check_in).days
            total_price = nights * listing.price_per_night

            booking = Booking(
                check_in=check_in,
                check_out=check_out,
                total_price=total_price,
                status=random.choice(["pending", "confirmed", "cancelled"]),
                client_id=client.id,
                listing_id=listing.id
            )

            bookings.append(booking)

    db.session.add_all(bookings)
    db.session.commit()

    print("Bookings seeded")
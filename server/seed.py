from werkzeug.security import generate_password_hash

from app import app

from models import ( db,  User, Listing, Booking, Review, Message,  PropertyImage, Amenity)
with app.app_context():

    print("Deleting old data...")

    Review.query.delete()
    Message.query.delete()
    Booking.query.delete()
    Amenity.query.delete()
    PropertyImage.query.delete()
    Listing.query.delete()
    User.query.delete()

    db.session.commit()

    print("Creating users...")

    host = User(
        username="John Host",
        email="host@safescape.com",
        phone="0712345678",
        password_hash=generate_password_hash("123456"),
        role="host"
    )

    guest = User(
        username="Mary Guest",
        email="guest@safescape.com",
        phone="0798765432",
        password_hash=generate_password_hash("123456"),
        role="guest"
    )

    db.session.add_all([host, guest])
    db.session.commit()

    print("Creating listings...")

    listing1 = Listing(
        title="Luxury Apartment",
        description="Modern apartment in Nairobi CBD.",
        country="Kenya",
        county="Nairobi",
        town="Nairobi",
        address="Kimathi Street",
        price_per_night=4500,
        bedrooms=2,
        bathrooms=1,
        max_guests=4,
        host_id=host.id
    )

    listing2 = Listing(
        title="Beach House",
        description="Relax by the ocean in Diani.",
        country="Kenya",
        county="Kwale",
        town="Diani",
        address="Beach Road",
        price_per_night=8500,
        bedrooms=3,
        bathrooms=2,
        max_guests=6,
        host_id=host.id
    )

    db.session.add_all([listing1, listing2])
    db.session.commit()

    print("Adding images...")

    img1 = PropertyImage(
        image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
        listing_id=listing1.id
    )

    img2 = PropertyImage(
        image_url="https://images.unsplash.com/photo-1494526585095-c41746248156",
        listing_id=listing2.id
    )

    db.session.add_all([img1, img2])

    print("Adding amenities...")

    amenities = [
        Amenity(name="WiFi", listing_id=listing1.id),
        Amenity(name="Parking", listing_id=listing1.id),
        Amenity(name="Swimming Pool", listing_id=listing2.id),
        Amenity(name="Ocean View", listing_id=listing2.id),
    ]

    db.session.add_all(amenities)

    db.session.commit()

    print("Database seeded successfully!") 
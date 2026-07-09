from datetime import date, timedelta

from werkzeug.security import generate_password_hash

from app import app

from models import (
    db, User, Listing, Booking, Review, Message, PropertyImage, Amenity
)

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

    # ==================================================
    # USERS
    # ==================================================

    print("Creating users...")

    host1 = User(
        username="John Host",
        email="host@safescape.com",
        phone="0712345678",
        password_hash=generate_password_hash("123456"),
        role="host"
    )

    host2 = User(
        username="Grace Njeri",
        email="grace@safescape.com",
        phone="0722334455",
        password_hash=generate_password_hash("123456"),
        role="host"
    )

    guest1 = User(
        username="Mary Guest",
        email="guest@safescape.com",
        phone="0798765432",
        password_hash=generate_password_hash("123456"),
        role="guest"
    )

    guest2 = User(
        username="Brian Otieno",
        email="brian@safescape.com",
        phone="0711223344",
        password_hash=generate_password_hash("123456"),
        role="guest"
    )

    db.session.add_all([host1, host2, guest1, guest2])
    db.session.commit()

    # ==================================================
    # LISTINGS
    # ==================================================

    print("Creating listings...")

    listing1 = Listing(
        title="Luxury Apartment",
        description="Modern apartment in Nairobi CBD, walking distance "
                     "to major offices and restaurants.",
        country="Kenya",
        county="Nairobi",
        town="Nairobi",
        address="Kimathi Street",
        price_per_night=4500,
        bedrooms=2,
        bathrooms=1,
        max_guests=4,
        host_id=host1.id
    )

    listing2 = Listing(
        title="Beach House",
        description="Relax by the ocean in Diani, steps from white "
                     "sand beaches.",
        country="Kenya",
        county="Kwale",
        town="Diani",
        address="Beach Road",
        price_per_night=8500,
        bedrooms=3,
        bathrooms=2,
        max_guests=6,
        host_id=host1.id
    )

    listing3 = Listing(
        title="Lakeside Cottage",
        description="Cosy cottage overlooking Lake Naivasha, perfect "
                     "for a quiet weekend getaway.",
        country="Kenya",
        county="Nakuru",
        town="Naivasha",
        address="Moi South Lake Road",
        price_per_night=5200,
        bedrooms=2,
        bathrooms=1,
        max_guests=4,
        host_id=host2.id
    )

    listing4 = Listing(
        title="Coastal Villa",
        description="Spacious villa near Malindi's old town, with a "
                     "private pool and garden.",
        country="Kenya",
        county="Kilifi",
        town="Malindi",
        address="Casuarina Road",
        price_per_night=12000,
        bedrooms=4,
        bathrooms=3,
        max_guests=8,
        host_id=host2.id
    )

    listing5 = Listing(
        title="Mountain View Cabin",
        description="Wooden cabin with views of Mount Kenya, ideal "
                     "for hikers and nature lovers.",
        country="Kenya",
        county="Laikipia",
        town="Nanyuki",
        address="Nanyuki-Nyeri Road",
        price_per_night=6000,
        bedrooms=2,
        bathrooms=2,
        max_guests=5,
        host_id=host1.id
    )

    listing6 = Listing(
        title="Westlands City Studio",
        description="Compact, stylish studio in Westlands, close to "
                     "malls, cafes, and nightlife.",
        country="Kenya",
        county="Nairobi",
        town="Nairobi",
        address="Westlands Road",
        price_per_night=3200,
        bedrooms=1,
        bathrooms=1,
        max_guests=2,
        host_id=host2.id
    )

    listing7 = Listing(
        title="Maasai Mara Safari Lodge",
        description="Rustic lodge on the edge of the Maasai Mara, "
                     "with guided game drives available.",
        country="Kenya",
        county="Narok",
        town="Maasai Mara",
        address="Mara North Conservancy",
        price_per_night=15000,
        bedrooms=3,
        bathrooms=2,
        max_guests=6,
        host_id=host1.id
    )

    listing8 = Listing(
        title="Kisumu Lakeside Bungalow",
        description="Peaceful bungalow on the shores of Lake "
                     "Victoria, with a private jetty.",
        country="Kenya",
        county="Kisumu",
        town="Kisumu",
        address="Dunga Beach Road",
        price_per_night=4800,
        bedrooms=2,
        bathrooms=1,
        max_guests=4,
        host_id=host2.id
    )

    listings = [
        listing1, listing2, listing3, listing4,
        listing5, listing6, listing7, listing8
    ]

    db.session.add_all(listings)
    db.session.commit()

    # ==================================================
    # IMAGES
    # ==================================================

    print("Adding images...")

    image_urls = {
        listing1.id: "https://picsum.photos/seed/safescape-apartment/800/600",
        listing2.id: "https://picsum.photos/seed/safescape-beachhouse/800/600",
        listing3.id: "https://picsum.photos/seed/safescape-lakecottage/800/600",
        listing4.id: "https://picsum.photos/seed/safescape-coastalvilla/800/600",
        listing5.id: "https://picsum.photos/seed/safescape-mountaincabin/800/600",
        listing6.id: "https://picsum.photos/seed/safescape-citystudio/800/600",
        listing7.id: "https://picsum.photos/seed/safescape-safarilodge/800/600",
        listing8.id: "https://picsum.photos/seed/safescape-lakebungalow/800/600",
    }

    images = [
        PropertyImage(image_url=url, listing_id=listing_id)
        for listing_id, url in image_urls.items()
    ]

    db.session.add_all(images)

    # ==================================================
    # AMENITIES
    # ==================================================

    print("Adding amenities...")

    amenities = [
        Amenity(name="WiFi", listing_id=listing1.id),
        Amenity(name="Parking", listing_id=listing1.id),

        Amenity(name="Swimming Pool", listing_id=listing2.id),
        Amenity(name="Ocean View", listing_id=listing2.id),

        Amenity(name="WiFi", listing_id=listing3.id),
        Amenity(name="Lake View", listing_id=listing3.id),
        Amenity(name="Fireplace", listing_id=listing3.id),

        Amenity(name="Swimming Pool", listing_id=listing4.id),
        Amenity(name="Garden", listing_id=listing4.id),
        Amenity(name="Air Conditioning", listing_id=listing4.id),

        Amenity(name="Mountain View", listing_id=listing5.id),
        Amenity(name="Hot Shower", listing_id=listing5.id),
        Amenity(name="Backup Generator", listing_id=listing5.id),

        Amenity(name="WiFi", listing_id=listing6.id),
        Amenity(name="Gym Access", listing_id=listing6.id),
        Amenity(name="24/7 Security", listing_id=listing6.id),

        Amenity(name="Game Drives", listing_id=listing7.id),
        Amenity(name="Full Board Meals", listing_id=listing7.id),

        Amenity(name="WiFi", listing_id=listing8.id),
        Amenity(name="Private Jetty", listing_id=listing8.id),
        Amenity(name="Garden", listing_id=listing8.id),
    ]

    db.session.add_all(amenities)
    db.session.commit()

    # ==================================================
    # SAMPLE BOOKINGS
    # ==================================================

    print("Creating sample bookings...")

    today = date.today()

    booking1 = Booking(
        guest_id=guest1.id,
        listing_id=listing1.id,
        check_in=today + timedelta(days=10),
        check_out=today + timedelta(days=14),
        guests=2,
        total_price=listing1.price_per_night * 4,
        status="pending"
    )

    booking2 = Booking(
        guest_id=guest1.id,
        listing_id=listing2.id,
        check_in=today - timedelta(days=20),
        check_out=today - timedelta(days=15),
        guests=4,
        total_price=listing2.price_per_night * 5,
        status="confirmed"
    )

    booking3 = Booking(
        guest_id=guest2.id,
        listing_id=listing3.id,
        check_in=today + timedelta(days=5),
        check_out=today + timedelta(days=8),
        guests=2,
        total_price=listing3.price_per_night * 3,
        status="confirmed"
    )

    booking4 = Booking(
        guest_id=guest2.id,
        listing_id=listing5.id,
        check_in=today - timedelta(days=40),
        check_out=today - timedelta(days=35),
        guests=3,
        total_price=listing5.price_per_night * 5,
        status="cancelled"
    )

    db.session.add_all([booking1, booking2, booking3, booking4])
    db.session.commit()

    # ==================================================
    # SAMPLE REVIEWS
    # (only for the completed/confirmed past stay, matching
    # the "must have booked" rule enforced on the real endpoint)
    # ==================================================

    print("Adding sample reviews...")

    review1 = Review(
        guest_id=guest1.id,
        listing_id=listing2.id,
        rating=5,
        comment="Beautiful beachfront property, stunning views and "
                "very responsive host!"
    )

    db.session.add(review1)
    db.session.commit()

    print("Database seeded successfully!")

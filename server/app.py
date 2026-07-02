from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models import ( db,User, Listing, Booking, Review, Message, PropertyImage, Amenity )
from flask_jwt_extended import ( JWTManager, create_access_token, jwt_required, get_jwt_identity)
app = Flask(__name__)

# ==========================================================
# CONFIGURATION
# ==========================================================

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user_bnb:123Host!@localhost/bnb_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "dev_secret_key"
jwt = JWTManager(app)

db.init_app(app)
CORS(app)

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the SafeScape API"
    })

# ==========================================================
# REGISTER
# ==========================================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    required = [
        "username",
        "email",
        "phone",
        "password",
        "role"
    ]

    for field in required:
        if field not in data:
            return jsonify({
                "error": f"{field} is required."
            }), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "error": "Email already exists."
        }), 400

    if User.query.filter_by(phone=data["phone"]).first():
        return jsonify({
            "error": "Phone number already exists."
        }), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        phone=data["phone"],
        password_hash=generate_password_hash(data["password"]),
        role=data["role"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully.",
        "user": new_user.to_dict()
    }), 201

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity={
            "id": user.id,
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

# ==========================================================
# USERS
# ==========================================================

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        user.to_dict()
        for user in users
    ])

# ==========================================================
# GET SINGLE USER
# ==========================================================

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = User.query.get_or_404(user_id)

    return jsonify(user.to_dict())

# ==========================================================
# GET ALL LISTINGS
# ==========================================================

@app.route("/listings", methods=["GET"])
def get_listings():

    listings = Listing.query.all()

    return jsonify([
        listing.to_dict()
        for listing in listings
    ])


# ==========================================================
# GET SINGLE LISTING
# ==========================================================

@app.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    return jsonify(listing.to_dict())


# ==========================================================
# CREATE LISTING
# ==========================================================

@app.route("/listings", methods=["POST"])
def create_listing():

    data = request.get_json()

    required = [
        "title",
        "description",
        "county",
        "town",
        "address",
        "price_per_night",
        "bedrooms",
        "bathrooms",
        "max_guests",
        "host_id"
    ]

    for field in required:
        if field not in data:
            return jsonify({
                "error": f"{field} is required."
            }), 400

    host = User.query.get(data["host_id"])

    if not host:
        return jsonify({
            "error": "Host not found."
        }), 404

    if host.role != "host":
        return jsonify({
            "error": "Only hosts can create listings."
        }), 403

    listing = Listing(
        title=data["title"],
        description=data["description"],
        country=data.get("country", "Kenya"),
        county=data["county"],
        town=data["town"],
        address=data["address"],
        price_per_night=data["price_per_night"],
        bedrooms=data["bedrooms"],
        bathrooms=data["bathrooms"],
        max_guests=data["max_guests"],
        available=True,
        host_id=data["host_id"]
    )

    db.session.add(listing)
    db.session.commit()

    return jsonify({
        "message": "Listing created successfully.",
        "listing": listing.to_dict()
    }), 201


# ==========================================================
# UPDATE LISTING
# ==========================================================

@app.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    data = request.get_json()

    listing.title = data.get("title", listing.title)
    listing.description = data.get("description", listing.description)
    listing.country = data.get("country", listing.country)
    listing.county = data.get("county", listing.county)
    listing.town = data.get("town", listing.town)
    listing.address = data.get("address", listing.address)
    listing.price_per_night = data.get("price_per_night", listing.price_per_night)
    listing.bedrooms = data.get("bedrooms", listing.bedrooms)
    listing.bathrooms = data.get("bathrooms", listing.bathrooms)
    listing.max_guests = data.get("max_guests", listing.max_guests)
    listing.available = data.get("available", listing.available)

    db.session.commit()

    return jsonify({
        "message": "Listing updated successfully.",
        "listing": listing.to_dict()
    })


# ==========================================================
# DELETE LISTING
# ==========================================================

@app.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    db.session.delete(listing)
    db.session.commit()

    return jsonify({
        "message": "Listing deleted successfully."
    })


# ==========================================================
# ADD PROPERTY IMAGE
# ==========================================================

@app.route("/listings/<int:listing_id>/images", methods=["POST"])
def add_image(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    data = request.get_json()

    if "image_url" not in data:
        return jsonify({
            "error": "image_url is required."
        }), 400

    image = PropertyImage(
        image_url=data["image_url"],
        listing_id=listing.id
    )

    db.session.add(image)
    db.session.commit()

    return jsonify({
        "message": "Image added successfully.",
        "image": image.to_dict()
    }), 201


# ==========================================================
# DELETE PROPERTY IMAGE
# ==========================================================

@app.route("/images/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):

    image = PropertyImage.query.get_or_404(image_id)

    db.session.delete(image)
    db.session.commit()

    return jsonify({
        "message": "Image deleted successfully."
    })


# ==========================================================
# ADD AMENITY
# ==========================================================

@app.route("/listings/<int:listing_id>/amenities", methods=["POST"])
def add_amenity(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    data = request.get_json()

    if "name" not in data:
        return jsonify({
            "error": "Amenity name is required."
        }), 400

    amenity = Amenity(
        name=data["name"],
        listing_id=listing.id
    )

    db.session.add(amenity)
    db.session.commit()

    return jsonify({
        "message": "Amenity added successfully.",
        "amenity": amenity.to_dict()
    }), 201


# ==========================================================
# DELETE AMENITY
# ==========================================================

@app.route("/amenities/<int:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):

    amenity = Amenity.query.get_or_404(amenity_id)

    db.session.delete(amenity)
    db.session.commit()

    return jsonify({
        "message": "Amenity deleted successfully."
    })

# ==========================================================
# CREATE BOOKING
# ==========================================================

@app.route("/bookings", methods=["POST"])
def create_booking():

    data = request.get_json()

    required = [
        "guest_id",
        "listing_id",
        "check_in",
        "check_out"
    ]

    for field in required:
        if field not in data:
            return jsonify({
                "error": f"{field} is required."
            }), 400

    guest = User.query.get(data["guest_id"])
    listing = Listing.query.get(data["listing_id"])

    if guest is None:
        return jsonify({"error": "Guest not found."}), 404

    if listing is None:
        return jsonify({"error": "Listing not found."}), 404

    if guest.role != "guest":
        return jsonify({"error": "Only guests can make bookings."}), 403

    check_in = datetime.strptime(
        data["check_in"],
        "%Y-%m-%d"
    ).date()

    check_out = datetime.strptime(
        data["check_out"],
        "%Y-%m-%d"
    ).date()

    if check_out <= check_in:
        return jsonify({
            "error": "Check-out must be after check-in."
        }), 400

    nights = (check_out - check_in).days

    total = nights * listing.price_per_night

    booking = Booking(
        guest_id=guest.id,
        listing_id=listing.id,
        check_in=check_in,
        check_out=check_out,
        guests=data.get("guests", 1),
        special_requests=data.get("special_requests", ""),
        total_price=total
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking created successfully.",
        "booking": booking.to_dict()
    }), 201


# ==========================================================
# GET BOOKINGS FOR A GUEST
# ==========================================================

@app.route("/bookings/guest/<int:guest_id>", methods=["GET"])
def guest_bookings(guest_id):

    bookings = Booking.query.filter_by(
        guest_id=guest_id
    ).all()

    return jsonify([
        booking.to_dict()
        for booking in bookings
    ])


# ==========================================================
# GET BOOKINGS FOR A HOST
# ==========================================================

@app.route("/bookings/host/<int:host_id>", methods=["GET"])
def host_bookings(host_id):

    bookings = Booking.query.join(Listing).filter(
        Listing.host_id == host_id
    ).all()

    return jsonify([
        booking.to_dict()
        for booking in bookings
    ])


# ==========================================================
# UPDATE BOOKING STATUS
# ==========================================================

@app.route("/bookings/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    data = request.get_json()

    booking.status = data.get(
        "status",
        booking.status
    )

    db.session.commit()

    return jsonify({
        "message": "Booking updated.",
        "booking": booking.to_dict()
    })


# ==========================================================
# DELETE BOOKING
# ==========================================================

@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    db.session.delete(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking cancelled."
    })


# ==========================================================
# CREATE REVIEW
# ==========================================================

@app.route("/reviews", methods=["POST"])
def create_review():

    data = request.get_json()

    review = Review(
        rating=data["rating"],
        comment=data.get("comment", ""),
        guest_id=data["guest_id"],
        listing_id=data["listing_id"]
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "Review added.",
        "review": review.to_dict()
    }), 201


# ==========================================================
# GET REVIEWS FOR A LISTING
# ==========================================================

@app.route("/reviews/<int:listing_id>", methods=["GET"])
def get_reviews(listing_id):

    reviews = Review.query.filter_by(
        listing_id=listing_id
    ).all()

    return jsonify([
        review.to_dict()
        for review in reviews
    ])


# ==========================================================
# SEND MESSAGE
# ==========================================================

@app.route("/messages", methods=["POST"])
def send_message():

    data = request.get_json()

    message = Message(
        sender_id=data["sender_id"],
        receiver_id=data["receiver_id"],
        message=data["message"]
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({
        "message": "Message sent.",
        "data": message.to_dict()
    }), 201


# ==========================================================
# GET CONVERSATION
# ==========================================================

@app.route("/messages/<int:user1>/<int:user2>", methods=["GET"])
def conversation(user1, user2):

    messages = Message.query.filter(
        ((Message.sender_id == user1) &
         (Message.receiver_id == user2))
        |
        ((Message.sender_id == user2) &
         (Message.receiver_id == user1))
    ).order_by(Message.sent_at.asc()).all()

    return jsonify([
        message.to_dict()
        for message in messages
    ])


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )

    
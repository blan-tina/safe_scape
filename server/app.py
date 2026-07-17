from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from models import db , User, Listing, Booking, Review, Message, PropertyImage, Amenity  
from flask_jwt_extended import ( JWTManager, create_access_token, jwt_required, get_jwt_identity)
from dotenv import load_dotenv 
import os 
load_dotenv()
app = Flask(__name__)

# ==========================================================
# CONFIGURATION
# ==========================================================

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

db.init_app(app)
migrate=Migrate(app,db)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:3000"
        }
    },
    supports_credentials=True
)


# ==========================================================
# HOME
# ==========================================================
@app.route("/")
def home():

    return jsonify({

        "message": "Welcome to the SafeScape API",

        "status": "Running"

    })

# ==========================================================
# REGISTER
# ==========================================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    required_fields = [
        "username",
        "email",
        "phone",
        "password",
        "role"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required."
            }), 400

    existing_user = User.query.filter(
        (User.email == data["email"]) |
        (User.phone == data["phone"])
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email or phone already exists."
        }), 409

    user = User(
        username=data["username"],
        email=data["email"],
        phone=data["phone"],
        password_hash=generate_password_hash(
            data["password"]
        ),
        role=data["role"]
    )

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity={
            "id": user.id,
            "role": user.role
        }
    )

    return jsonify({
        "message": "Account created successfully.",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        }
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

    user = User.query.filter_by(
        email=email
    ).first()

    if (
        not user or
        not check_password_hash(
            user.password_hash,
            password
        )
    ):

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

        "access_token": access_token,

        "user": {

            "id": user.id,

            "username": user.username,

            "email": user.email,

            "phone": user.phone,

            "role": user.role

        }

    })

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

    query = Listing.query.filter(Listing.available == True)

    location = request.args.get("location")

    if location:
        search_term = f"%{location}%"
        query = query.filter(
            db.or_(
                Listing.town.ilike(search_term),
                Listing.county.ilike(search_term),
                Listing.country.ilike(search_term),
                Listing.title.ilike(search_term),
            )
        )

    guests = request.args.get("guests")

    if guests:
        try:
            query = query.filter(Listing.max_guests >= int(guests))
        except ValueError:
            pass

    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")

    if check_in and check_out:
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            conflicting_listing_ids = db.session.query(
                Booking.listing_id
            ).filter(
                Booking.status != "cancelled",
                Booking.check_in < check_out_date,
                Booking.check_out > check_in_date,
            )

            query = query.filter(
                Listing.id.notin_(conflicting_listing_ids)
            )
        except ValueError:
            pass

    listings = query.all()

    return jsonify([
        listing.to_dict()
        for listing in listings
    ])


# ==========================================================
# GET SINGLE LISTING
# ==========================================================
@app.route("/listings/<int:id>", methods=["GET"])
def get_listing(id):

    listing = Listing.query.get(id)

    if not listing:
        return jsonify({
            "error": "Property not found."
        }), 404

    return jsonify({

        "id": listing.id,

        "title": listing.title,

        "description": listing.description,

        "country": listing.country,

        "county": listing.county,

        "town": listing.town,

        "address": listing.address,

        "price_per_night": listing.price_per_night,

        "bedrooms": listing.bedrooms,

        "bathrooms": listing.bathrooms,

        "max_guests": listing.max_guests,

        "available": listing.available,

        "host": listing.host.username,

        "host_id": listing.host_id,

        "images": [
            {"id": image.id, "image_url": image.image_url}
            for image in listing.images
        ],

        "amenities": [
            {"id": amenity.id, "name": amenity.name}
            for amenity in listing.amenities
        ],

        "average_rating": round(
            sum(r.rating for r in listing.reviews) / len(listing.reviews), 1
        ) if listing.reviews else None,

        "review_count": len(listing.reviews),

        "reviews": [
            {
                "id": review.id,
                "guest": review.guest.username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat()
            }
            for review in listing.reviews
        ]

    })

#=======================================================
# GET LISTINGS FOR A HOST
#=======================================================
@app.route("/my-listings", methods=["GET"])
@jwt_required()
def my_listings():

    current_user = get_jwt_identity()

    host = User.query.get(current_user["id"])

    if not host:
        return jsonify({
            "error": "User not found."
        }), 404

    listings = []

    for listing in host.listings:

        listings.append({

            "id": listing.id,

            "title": listing.title,

            "county": listing.county,

            "town": listing.town,

            "price_per_night": listing.price_per_night,

            "bookings": len(listing.bookings),

            "image": (
                listing.images[0].image_url
                if listing.images
                else "https://placehold.co/600x400?text=No+Image"
            )

        })

    return jsonify(listings)
# ==========================================================
# CREATE LISTING
# ==========================================================

@app.route("/listings", methods=["POST"])
@jwt_required()
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
        
    ]

    for field in required:
        if field not in data:
            return jsonify({
                "error": f"{field} is required."
            }), 400

    current_user = get_jwt_identity()

    host = User.query.get(current_user["id"])

    if not host:
        return jsonify({
            "error": "User not found."
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
        host_id=host.id
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
@jwt_required()
def update_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    current_user = get_jwt_identity()

    if listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only edit your own properties."
        }), 403

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
@jwt_required()
def delete_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    current_user = get_jwt_identity()

    if listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only delete your own properties."
        }), 403

    db.session.delete(listing)
    db.session.commit()

    return jsonify({
        "message": "Listing deleted successfully."
    })


# ==========================================================
# ADD PROPERTY IMAGE
# ==========================================================

@app.route("/listings/<int:listing_id>/images", methods=["POST"])
@jwt_required()
def add_image(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    current_user = get_jwt_identity()

    if listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only add images to your own properties."
        }), 403

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
@jwt_required()
def delete_image(image_id):

    image = PropertyImage.query.get_or_404(image_id)

    current_user = get_jwt_identity()

    if image.listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only delete images from your own properties."
        }), 403

    db.session.delete(image)
    db.session.commit()

    return jsonify({
        "message": "Image deleted successfully."
    })


# ==========================================================
# ADD AMENITY
# ==========================================================

@app.route("/listings/<int:listing_id>/amenities", methods=["POST"])
@jwt_required()
def add_amenity(listing_id):

    listing = Listing.query.get_or_404(listing_id)

    current_user = get_jwt_identity()

    if listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only add amenities to your own properties."
        }), 403

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
@jwt_required()
def delete_amenity(amenity_id):

    amenity = Amenity.query.get_or_404(amenity_id)

    current_user = get_jwt_identity()

    if amenity.listing.host_id != current_user["id"]:
        return jsonify({
            "error": "You can only delete amenities from your own properties."
        }), 403

    db.session.delete(amenity)
    db.session.commit()

    return jsonify({
        "message": "Amenity deleted successfully."
    })

# ==========================================================
# CREATE BOOKING
# ==========================================================

@app.route("/bookings", methods=["POST"])
@jwt_required()
def create_booking():

    data = request.get_json()

    current_user = get_jwt_identity()
    guest_id = current_user["id"]

    listing_id = data.get("listing_id")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    guests = data.get("guests", 1)

    # -----------------------
    # Validate required fields
    # -----------------------
    if not listing_id or not check_in or not check_out:
        return jsonify({
            "error": "All booking fields are required."
        }), 400

    # -----------------------
    # Convert dates
    # -----------------------
    try:
        check_in = datetime.strptime(
            check_in,
            "%Y-%m-%d"
        ).date()

        check_out = datetime.strptime(
            check_out,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return jsonify({
            "error": "Invalid date format."
        }), 400

    # -----------------------
    # Check dates
    # -----------------------
    if check_out <= check_in:
        return jsonify({
            "error": "Check-out must be after check-in."
        }), 400

    # -----------------------
    # Only guests can book
    # -----------------------
    guest = User.query.get(guest_id)

    if not guest or guest.role != "guest":
        return jsonify({
            "error": "Only guests can book properties."
        }), 403

    # -----------------------
    # Find property
    # -----------------------
    listing = Listing.query.get(listing_id)

    if not listing:
        return jsonify({
            "error": "Property not found."
        }), 404

    # -----------------------
    # Prevent double booking
    # -----------------------
    existing_booking = Booking.query.filter(
        Booking.listing_id == listing_id,
        Booking.status != "cancelled",
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).first()

    if existing_booking:
        return jsonify({
            "error": "These dates are already booked."
        }), 400

    # -----------------------
    # Calculate price
    # -----------------------
    nights = (check_out - check_in).days

    total_price = nights * listing.price_per_night

    # -----------------------
    # Create booking
    # -----------------------
    booking = Booking(
        guest_id=guest_id,
        listing_id=listing_id,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        total_price=total_price,
        status="pending"
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking created successfully.",
        "booking": booking.to_dict()
    }), 201

# ==========================================================
# GET MY BOOKINGS
# ==========================================================

@app.route("/my-bookings", methods=["GET"])
@jwt_required()
def my_bookings():

    current_user = get_jwt_identity()

    bookings = Booking.query.filter_by(
        guest_id=current_user["id"]
    ).all()

    results = []

    for booking in bookings:

        listing = booking.listing

        results.append({

            "id": booking.id,

            "check_in": booking.check_in.isoformat(),

            "check_out": booking.check_out.isoformat(),

            "guests": booking.guests,

            "status": booking.status,

            "total_price": booking.total_price,

            "title": listing.title,

            "town": listing.town,

            "county": listing.county,

            "price_per_night": listing.price_per_night,

            "image": (
                listing.images[0].image_url
                if listing.images
                else "https://placehold.co/600x400"
            )

        })

    return jsonify(results)
# ==========================================================
# GET BOOKINGS FOR A GUEST
# ==========================================================

@app.route("/bookings/guest/<int:guest_id>", methods=["GET"])
@jwt_required()
def guest_bookings(guest_id):

    current_user = get_jwt_identity()

    if current_user["id"] != guest_id:
        return jsonify({
            "error": "You can only view your own bookings."
        }), 403

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
@jwt_required()
def host_bookings(host_id):

    current_user = get_jwt_identity()

    if current_user["id"] != host_id:
        return jsonify({
            "error": "You can only view your own bookings."
        }), 403

    bookings = Booking.query.join(Listing).filter(
        Listing.host_id == host_id
    ).all()

    return jsonify([
        booking.to_dict()
        for booking in bookings
    ])


# ==========================================================
# GET MY BOOKINGS (AS HOST) - for the host dashboard
# ==========================================================

@app.route("/host-bookings", methods=["GET"])
@jwt_required()
def my_host_bookings():

    current_user = get_jwt_identity()

    bookings = Booking.query.join(Listing).filter(
        Listing.host_id == current_user["id"]
    ).order_by(Booking.created_at.desc()).all()

    return jsonify([
        {
            "id": booking.id,
            "listing_id": booking.listing_id,
            "listing_title": booking.listing.title,
            "guest_name": booking.guest.username,
            "check_in": booking.check_in.isoformat(),
            "check_out": booking.check_out.isoformat(),
            "guests": booking.guests,
            "total_price": booking.total_price,
            "status": booking.status,
        }
        for booking in bookings
    ])


# ==========================================================
# UPDATE BOOKING STATUS
# ==========================================================

@app.route("/bookings/<int:booking_id>", methods=["PUT"])
@jwt_required()
def update_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    current_user = get_jwt_identity()

    if booking.listing.host_id != current_user["id"]:
        return jsonify({
            "error": "Only the property host can update this booking."
        }), 403

    data = request.get_json()

    new_status = data.get("status", booking.status)

    allowed_statuses = ["pending", "confirmed", "cancelled"]

    if new_status not in allowed_statuses:
        return jsonify({
            "error": f"status must be one of {allowed_statuses}."
        }), 400

    booking.status = new_status

    db.session.commit()

    return jsonify({
        "message": "Booking updated.",
        "booking": booking.to_dict()
    })


# ==========================================================
# DELETE BOOKING
# ==========================================================

@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    current_user = get_jwt_identity()

    if current_user["id"] not in (booking.guest_id, booking.listing.host_id):
        return jsonify({
            "error": "Unauthorized"
        }), 403

    db.session.delete(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking cancelled."
    })

#=========================================================
# CANCEL BOOKING ROUTE
#=========================================================
@app.route("/bookings/<int:id>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_booking(id):

    identity = get_jwt_identity()

    booking = Booking.query.get_or_404(id)

    if booking.guest_id != identity["id"]:
        return jsonify({
            "error": "Unauthorized"
        }), 403

    booking.status = "cancelled"

    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully."
    })

# ==========================================================
# CREATE REVIEW
# ==========================================================

@app.route("/reviews", methods=["POST"])
@jwt_required()
def create_review():

    data = request.get_json()

    if not data.get("rating") or not data.get("listing_id"):
        return jsonify({
            "error": "rating and listing_id are required."
        }), 400

    if not (1 <= int(data["rating"]) <= 5):
        return jsonify({
            "error": "rating must be between 1 and 5."
        }), 400

    listing = Listing.query.get(data["listing_id"])

    if not listing:
        return jsonify({
            "error": "Property not found."
        }), 404

    current_user = get_jwt_identity()

    # Only guests who have actually booked this property may review it.
    has_booking = Booking.query.filter(
        Booking.listing_id == data["listing_id"],
        Booking.guest_id == current_user["id"],
        Booking.status != "cancelled",
    ).first()

    if not has_booking:
        return jsonify({
            "error": "You can only review properties you have booked."
        }), 403

    # Prevent leaving more than one review per listing.
    existing_review = Review.query.filter_by(
        listing_id=data["listing_id"],
        guest_id=current_user["id"],
    ).first()

    if existing_review:
        return jsonify({
            "error": "You have already reviewed this property."
        }), 400

    review = Review(
        rating=data["rating"],
        comment=data.get("comment", ""),
        guest_id=current_user["id"],
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
@jwt_required()
def send_message():

    data = request.get_json()

    if not data.get("receiver_id") or not data.get("message"):
        return jsonify({
            "error": "receiver_id and message are required."
        }), 400

    receiver = User.query.get(data["receiver_id"])

    if not receiver:
        return jsonify({
            "error": "Recipient not found."
        }), 404

    current_user = get_jwt_identity()

    message = Message(
        sender_id=current_user["id"],
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
@jwt_required()
def conversation(user1, user2):

    current_user = get_jwt_identity()

    if current_user["id"] not in (user1, user2):
        return jsonify({
            "error": "You can only view your own conversations."
        }), 403

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
# INBOX - LIST ALL CONVERSATIONS FOR CURRENT USER
# ==========================================================

@app.route("/conversations", methods=["GET"])
@jwt_required()
def list_conversations():

    current_user = get_jwt_identity()
    my_id = current_user["id"]

    messages = Message.query.filter(
        (Message.sender_id == my_id) |
        (Message.receiver_id == my_id)
    ).order_by(Message.sent_at.desc()).all()

    conversations = {}

    for msg in messages:

        other_user = msg.receiver if msg.sender_id == my_id else msg.sender

        if other_user.id not in conversations:
            conversations[other_user.id] = {
                "user_id": other_user.id,
                "username": other_user.username,
                "last_message": msg.message,
                "last_message_at": msg.sent_at.isoformat(),
            }

    return jsonify(list(conversations.values()))


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        use_reloader=False,
        host="0.0.0.0",
        port=5000
    )

    
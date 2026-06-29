from flask import Flask, jsonify, request
from models import db, User, BNBListing, Booking
from datetime import datetime
import os

app = Flask(__name__)

# --------------------
# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user_bnb:123Host!@localhost/bnb_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "dev_secret_key"

db.init_app(app)


# --------------------
# HOME ROUTE
# --------------------
@app.route("/")
def home():
    return jsonify({
        "message": "BNB Platform API is running"
    })


# --------------------
# GET ALL LISTINGS
# --------------------
@app.route("/listings", methods=["GET"])
def get_listings():
    listings = BNBListing.query.all()

    return jsonify([
        {
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "location": l.location,
            "price_per_night": l.price_per_night,
            "host_id": l.host_id
        }
        for l in listings
    ])


# --------------------
# CREATE LISTING (HOST ONLY)
# --------------------
@app.route("/listings", methods=["POST"])
def create_listing():
    data = request.get_json()

    listing = BNBListing(
        title=data["title"],
        description=data["description"],
        location=data["location"],
        price_per_night=data["price_per_night"],
        host_id=data["host_id"]
    )

    db.session.add(listing)
    db.session.commit()

    return jsonify({"message": "Listing created successfully"}), 201


# --------------------
# BOOK A LISTING (CLIENT)
# --------------------
@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()

    check_in = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
    check_out = datetime.strptime(data["check_out"], "%Y-%m-%d").date()

    listing = BNBListing.query.get(data["listing_id"])

    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    nights = (check_out - check_in).days
    total_price = nights * listing.price_per_night

    booking = Booking(
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
        status="pending",
        client_id=data["client_id"],
        listing_id=data["listing_id"]
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking successful"}), 201


# --------------------
# GET BOOKINGS (CLIENT VIEW)
# --------------------
@app.route("/bookings/<int:user_id>", methods=["GET"])
def get_bookings(user_id):
    bookings = Booking.query.filter_by(client_id=user_id).all()

    return jsonify([
        {
            "id": b.id,
            "listing_id": b.listing_id,
            "check_in": str(b.check_in),
            "check_out": str(b.check_out),
            "total_price": b.total_price,
            "status": b.status
        }
        for b in bookings
    ])


# --------------------
# RUN APP
# --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    
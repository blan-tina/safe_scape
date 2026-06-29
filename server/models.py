from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# --------------------
# USER MODEL (Host or Client)
# --------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="client")
    # roles: client | host

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # If user is a host → has listings
    listings = db.relationship(
        "BNBListing",
        back_populates="host",
        cascade="all, delete-orphan"
    )

    # If user is a client → has bookings
    bookings = db.relationship(
        "Booking",
        back_populates="client",
        cascade="all, delete-orphan"
    )


# --------------------
# BNB LISTING MODEL (for Host)
# --------------------
class BNBListing(db.Model):
    __tablename__ = "bnb_listings"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    location = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)

    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    host = db.relationship("User", back_populates="listings")

    bookings = db.relationship(
        "Booking",
        back_populates="listing",
        cascade="all, delete-orphan"
    )


# --------------------
# BOOKING MODEL (for  Client)
# --------------------
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(20), default="pending")
    # pending | confirmed | cancelled

    client_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("bnb_listings.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("User", back_populates="bookings")
    listing = db.relationship("BNBListing", back_populates="bookings")
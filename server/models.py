from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ======================================================
# USER MODEL
# ======================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)  # guest | host

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship(
        "Listing",
        back_populates="host",
        cascade="all, delete-orphan"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

    sent_messages = db.relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    received_messages = db.relationship(
        "Message",
        foreign_keys="Message.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }


# ======================================================
# LISTING MODEL
# ======================================================

class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    country = db.Column(db.String(100), default="Kenya")
    county = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    price_per_night = db.Column(db.Float, nullable=False)

    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    available = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    host_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    host = db.relationship(
        "User",
        back_populates="listings"
    )

    images = db.relationship(
        "PropertyImage",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "country": self.country,
            "county": self.county,
            "town": self.town,
            "address": self.address,
            "price_per_night": self.price_per_night,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "max_guests": self.max_guests,
            "available": self.available,
            "host": self.host.username,
            "host_id": self.host_id,
            "images": [
                {"id": image.id, "image_url": image.image_url}
                for image in self.images
            ],
            "amenities": [
                {"id": amenity.id, "name": amenity.name}
                for amenity in self.amenities
            ],
            "created_at": self.created_at.isoformat()
        }


# ======================================================
# PROPERTY IMAGES
# ======================================================

class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(db.Integer, primary_key=True)

    image_url = db.Column(db.String(500), nullable=False)

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listings.id"),
        nullable=False
    )

    listing = db.relationship(
        "Listing",
        back_populates="images"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "listing_id": self.listing_id
        }


# ======================================================
# AMENITIES
# ======================================================

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listings.id"),
        nullable=False
    )

    listing = db.relationship(
        "Listing",
        back_populates="amenities"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "listing_id": self.listing_id
        }


# ======================================================
# BOOKINGS
# ======================================================

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    guests = db.Column(db.Integer, default=1)

    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    special_requests = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    guest_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listings.id"),
        nullable=False
    )

    guest = db.relationship(
        "User",
        back_populates="bookings"
    )

    listing = db.relationship(
        "Listing",
        back_populates="bookings"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "guests": self.guests,
            "total_price": self.total_price,
            "status": self.status,
            "special_requests": self.special_requests,
            "guest_id": self.guest_id,
            "guest": self.guest.username,
            "listing_id": self.listing_id,
            "listing": self.listing.title,
            "created_at": self.created_at.isoformat()
        }


# ======================================================
# REVIEWS
# ======================================================

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    guest_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listings.id"),
        nullable=False
    )

    guest = db.relationship(
        "User",
        back_populates="reviews"
    )

    listing = db.relationship(
        "Listing",
        back_populates="reviews"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "guest": self.guest.username,
            "guest_id": self.guest_id,
            "listing_id": self.listing_id,
            "listing": self.listing.title,
            "created_at": self.created_at.isoformat()
        }


# ======================================================
# MESSAGES
# ======================================================

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)

    sent_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_messages"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "sender_id": self.sender_id,
            "sender": self.sender.username,
            "receiver_id": self.receiver_id,
            "receiver": self.receiver.username,
            "sent_at": self.sent_at.isoformat()
        }
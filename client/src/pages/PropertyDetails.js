import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./PropertyDetails.css";

function PropertyDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);

  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState(1);

  useEffect(() => {
    api
      .get(`/listings/${id}`)
      .then((res) => {
        setProperty(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="property-details">
        <h2>Loading property...</h2>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="property-details">
        <h2>Property not found.</h2>
      </div>
    );
  }

  const totalNights =
    checkIn && checkOut
      ? Math.max(
          0,
          (new Date(checkOut) - new Date(checkIn)) /
            (1000 * 60 * 60 * 24)
        )
      : 0;

  const totalPrice = totalNights * property.price_per_night;

  async function handleReserve() {
    if (!user) {
      alert("Please login first.");
      navigate("/login");
      return;
    }

    if (user.role !== "guest") {
      alert("Only guests can reserve properties.");
      return;
    }

    if (!checkIn || !checkOut) {
      alert("Please select your check-in and check-out dates.");
      return;
    }

    if (new Date(checkOut) <= new Date(checkIn)) {
      alert("Check-out must be after check-in.");
      return;
    }

    if (guests > property.max_guests) {
      alert(
        `Maximum guests allowed is ${property.max_guests}.`
      );
      return;
    }

    try {
      await api.post("/bookings", {
        listing_id: property.id,
        guest_id: user.id,
        check_in: checkIn,
        check_out: checkOut,
        guests: guests,
      });

      alert("🎉 Booking created successfully!");

      navigate("/guest-dashboard");
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.error ||
          "Booking failed."
      );
    }
  }

  return (
    <div className="property-details">

      <h1 className="property-title">
        {property.title}
      </h1>

      <p className="property-location">
        📍 {property.town}, {property.county}, {property.country}
      </p>

      <img
        src={
          property.images && property.images.length > 0
            ? property.images[0]
            : "https://placehold.co/900x500?text=No+Image"
        }
        alt={property.title}
        className="hero-image"
      />

      <div className="property-content">

        <div className="left-column">

          <h2>About this Property</h2>

          <p>{property.description}</p>

          <div className="features">

            <span>
              🛏 {property.bedrooms} Bedrooms
            </span>

            <span>
              🚿 {property.bathrooms} Bathrooms
            </span>

            <span>
              👨‍👩‍👧 {property.max_guests} Guests
            </span>

          </div>

          <h2>Amenities</h2>

          <div className="amenities">

            {property.amenities &&
              property.amenities.map((amenity, index) => (
                <div
                  className="amenity"
                  key={index}
                >
                  ✔ {amenity}
                </div>
              ))}

          </div>

          <h2 style={{ marginTop: "50px" }}>
            Hosted by {property.host}
          </h2>

        </div>

        <div className="booking-card">

          <h2>
            KSh {property.price_per_night.toLocaleString()}
          </h2>

          <p>per night</p>

          <hr />

          <label>Check In</label>

          <input
            type="date"
            value={checkIn}
            onChange={(e) =>
              setCheckIn(e.target.value)
            }
          />

          <label>Check Out</label>

          <input
            type="date"
            value={checkOut}
            onChange={(e) =>
              setCheckOut(e.target.value)
            }
          />

          <label>Guests</label>

          <select
            value={guests}
            onChange={(e) =>
              setGuests(Number(e.target.value))
            }
          >
            {Array.from(
              { length: property.max_guests },
              (_, i) => i + 1
            ).map((num) => (
              <option
                key={num}
                value={num}
              >
                {num} Guest{num > 1 ? "s" : ""}
              </option>
            ))}
          </select>

          <hr />

          <p>
            <strong>Nights:</strong> {totalNights}
          </p>

          <p>
            <strong>Total Price</strong>
          </p>

          <h2
            style={{
              color: "#2E7D32",
              marginBottom: "20px",
            }}
          >
            KSh {totalPrice.toLocaleString()}
          </h2>

          <button
            className="reserve-btn"
            onClick={handleReserve}
          >
            Reserve Now
          </button>

        </div>

      </div>

    </div>
  );
}

export default PropertyDetails;
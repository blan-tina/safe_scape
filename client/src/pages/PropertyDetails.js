import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

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

  const [reviewRating, setReviewRating] = useState(5);
  const [reviewComment, setReviewComment] = useState("");
  const [reviewError, setReviewError] = useState("");
  const [reviewSubmitting, setReviewSubmitting] = useState(false);

  const [messageText, setMessageText] = useState("");
  const [messageError, setMessageError] = useState("");
  const [messageSuccess, setMessageSuccess] = useState("");
  const [messageSending, setMessageSending] = useState(false);

  function fetchProperty() {
    return api.get(`/listings/${id}`).then((res) => {
      setProperty(res.data);
    });
  }

  useEffect(() => {
    fetchProperty()
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  async function handleSubmitReview(e) {
    e.preventDefault();

    setReviewError("");
    setReviewSubmitting(true);

    try {
      await api.post("/reviews", {
        listing_id: property.id,
        rating: reviewRating,
        comment: reviewComment,
      });

      setReviewComment("");
      setReviewRating(5);

      await fetchProperty();
    } catch (err) {
      setReviewError(
        err.response?.data?.error || "Unable to submit review."
      );
    } finally {
      setReviewSubmitting(false);
    }
  }

  async function handleSendMessage(e) {
    e.preventDefault();

    if (!user) {
      alert("Please login to message the host.");
      navigate("/login");
      return;
    }

    setMessageError("");
    setMessageSuccess("");
    setMessageSending(true);

    try {
      await api.post("/messages", {
        receiver_id: property.host_id,
        message: messageText,
      });

      setMessageText("");
      setMessageSuccess("Message sent!");
    } catch (err) {
      setMessageError(
        err.response?.data?.error || "Unable to send message."
      );
    } finally {
      setMessageSending(false);
    }
  }

  return (
    <div className="property-details">

      <h1 className="property-title">
        {property.title}
      </h1>

      <p className="property-rating-summary">
        {property.average_rating
          ? `⭐ ${property.average_rating} · ${property.review_count} review${property.review_count === 1 ? "" : "s"}`
          : "New listing · No reviews yet"}
      </p>

      <p className="property-location">
        📍 {property.town}, {property.county}, {property.country}
      </p>

      <img
        src={
          property.images && property.images.length > 0
            ? property.images[0].image_url
            : "https://placehold.co/900x500?text=No+Image"
        }
        alt={property.title}
        className="hero-image"
        onError={(e) => {
          e.target.onerror = null;
          e.target.src = "https://placehold.co/900x500?text=No+Image";
        }}
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
              property.amenities.map((amenity) => (
                <div
                  className="amenity"
                  key={amenity.id}
                >
                  ✔ {amenity.name}
                </div>
              ))}

          </div>

          <h2 style={{ marginTop: "50px" }}>
            Hosted by {property.host}
          </h2>

          {user && user.id !== property.host_id && (
            <div className="message-host-box">

              <h3>Message the Host</h3>

              {messageSuccess && (
                <p className="form-success">{messageSuccess}</p>
              )}

              {messageError && (
                <p className="form-error">{messageError}</p>
              )}

              <form onSubmit={handleSendMessage}>
                <textarea
                  rows="3"
                  placeholder={`Ask ${property.host} a question about this property...`}
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  required
                />

                <button type="submit" disabled={messageSending}>
                  {messageSending ? "Sending..." : "Send Message"}
                </button>
              </form>

              <Link
                to={`/messages/${property.host_id}`}
                className="view-conversation-link"
              >
                View full conversation →
              </Link>

            </div>
          )}

          <h2 style={{ marginTop: "50px" }}>
            Reviews
            {property.review_count > 0 && ` (${property.review_count})`}
          </h2>

          {user && user.role === "guest" && (
            <form
              className="review-form"
              onSubmit={handleSubmitReview}
            >
              {reviewError && (
                <p className="form-error">{reviewError}</p>
              )}

              <label>Your Rating</label>

              <select
                value={reviewRating}
                onChange={(e) => setReviewRating(Number(e.target.value))}
              >
                <option value="5">⭐⭐⭐⭐⭐ (5)</option>
                <option value="4">⭐⭐⭐⭐ (4)</option>
                <option value="3">⭐⭐⭐ (3)</option>
                <option value="2">⭐⭐ (2)</option>
                <option value="1">⭐ (1)</option>
              </select>

              <textarea
                rows="3"
                placeholder="Share your experience staying here..."
                value={reviewComment}
                onChange={(e) => setReviewComment(e.target.value)}
              />

              <button type="submit" disabled={reviewSubmitting}>
                {reviewSubmitting ? "Submitting..." : "Submit Review"}
              </button>

              <p className="review-hint">
                Only guests who have booked this property can leave a review.
              </p>
            </form>
          )}

          <div className="reviews-list">

            {property.reviews && property.reviews.length > 0 ? (
              property.reviews.map((review) => (
                <div className="review-item" key={review.id}>
                  <div className="review-header">
                    <strong>{review.guest}</strong>
                    <span>{"⭐".repeat(review.rating)}</span>
                  </div>

                  {review.comment && <p>{review.comment}</p>}

                  <span className="review-date">
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))
            ) : (
              <p>No reviews yet. Be the first to stay and share your experience!</p>
            )}

          </div>

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
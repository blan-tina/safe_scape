import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./GuestDashboard.css";

function GuestDashboard() {
  const { user } = useAuth();

  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookings();
  }, []);

  async function fetchBookings() {
    try {
      const response = await api.get("/my-bookings");
      setBookings(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function cancelBooking(id) {
    const confirmCancel = window.confirm(
      "Are you sure you want to cancel this booking?"
    );

    if (!confirmCancel) return;

    try {
      await api.patch(`/bookings/${id}/cancel`);

      fetchBookings();
    } catch (error) {
      console.error(error);
    }
  }

  if (loading) {
    return <h2>Loading your bookings...</h2>;
  }

  return (
    <div className="dashboard">

      <h1>Welcome back, {user.username} 👋</h1>

      <h2>My Bookings</h2>

      {bookings.length === 0 ? (
        <p>You haven't booked any properties yet.</p>
      ) : (
        bookings.map((booking) => (
          <div
            className="booking-card"
            key={booking.id}
          >
            <img
              src={booking.image}
              alt={booking.title}
            />

            <div className="booking-info">

              <h3>{booking.title}</h3>

              <p>
                📍 {booking.town}, {booking.county}
              </p>

              <p>
                Check In:
                {" "}
                {booking.check_in}
              </p>

              <p>
                Check Out:
                {" "}
                {booking.check_out}
              </p>

              <p>
                Guests:
                {" "}
                {booking.guests}
              </p>

              <p>
                Total:
                {" "}
                KSh {booking.total_price.toLocaleString()}
              </p>

              <p>
                Status:
                {" "}
                <strong>{booking.status}</strong>
              </p>

              {booking.status === "pending" && (
                <button
                  onClick={() =>
                    cancelBooking(booking.id)
                  }
                >
                  Cancel Booking
                </button>
              )}

            </div>

          </div>
        ))
      )}

    </div>
  );
}

export default GuestDashboard;
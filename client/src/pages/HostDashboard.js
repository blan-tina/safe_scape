import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./HostDashboard.css";

function HostDashboard() {
  const { user } = useAuth();

  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings();
  }, []);

  async function fetchListings() {
    try {
      const response = await api.get("/my-listings");
      setListings(response.data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }

  async function deleteListing(id) {
    const confirmDelete = window.confirm(
      "Delete this property?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`/listings/${id}`);

      fetchListings();

      alert("Property deleted successfully.");
    } catch (error) {
      console.log(error);

      alert(
        error.response?.data?.error ||
        "Unable to delete property."
      );
    }
  }

  if (loading) {
    return <h2>Loading dashboard...</h2>;
  }

  return (
    <div className="host-dashboard">

      <div className="dashboard-header">

        <div>
          <h1>Welcome back, {user.username} 👋</h1>
          <p>Manage all your SafeScape properties.</p>
        </div>

        <Link
          className="add-property-btn"
          to="/host/add-property"
        >
          + Add Property
        </Link>

      </div>

      <div className="stats">

        <div className="stat-card">
          <h3>{listings.length}</h3>
          <p>Total Listings</p>
        </div>

        <div className="stat-card">
          <h3>
            {
              listings.reduce(
                (sum, property) =>
                  sum + property.bookings,
                0
              )
            }
          </h3>
          <p>Total Bookings</p>
        </div>

      </div>

      <h2>My Properties</h2>

      <div className="host-properties">

        {listings.length === 0 ? (

          <p>You haven't added any properties yet.</p>

        ) : (

          listings.map((property) => (

            <div
              className="host-property-card"
              key={property.id}
            >

              <img
                src={property.image}
                alt={property.title}
              />

              <div className="property-info">

                <h3>{property.title}</h3>

                <p>
                  📍 {property.town}, {property.county}
                </p>

                <p>
                  KSh {property.price_per_night.toLocaleString()}
                  /night
                </p>

                <p>
                  {property.bookings} bookings
                </p>

              </div>

              <div className="actions">

                <Link
                  to={`/host/edit/${property.id}`}
                >
                  Edit
                </Link>

                <button
                  onClick={() =>
                    deleteListing(property.id)
                  }
                >
                  Delete
                </button>

              </div>

            </div>

          ))

        )}

      </div>

    </div>
  );
}

export default HostDashboard;
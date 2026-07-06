import "./PropertyCard.css";
import { Link } from "react-router-dom";

function PropertyCard({ property }) {
  return (
    <div className="property-card">

      <div className="image-container">

        <img
          src={
            property.images && property.images.length > 0
              ? property.images[0].image_url
              : "https://placehold.co/400x250?text=No+Image"
          }
          alt={property.title}
          className="property-image"
        />

        <span className="verified">
          ✔ Verified
        </span>

        <button className="favorite">
          ♡
        </button>

      </div>

      <div className="property-info">

        <div className="title-row">
          <h3>{property.title}</h3>

          <span className="rating">
            ⭐ 4.7
          </span>
        </div>

        <p className="location">
          📍 {property.town}, {property.county}
        </p>

        <p className="details">
          🛏 {property.bedrooms} Bedrooms • 🚿 {property.bathrooms} Bathrooms
        </p>

        <p className="amenities">
          {property.amenities?.map((a) => a.name).join(" • ")}
        </p>

        <div className="bottom-row">

          <div>

            <span className="price">
              KSh {property.price_per_night}
            </span>

            <span className="night">
              / night
            </span>

          </div>

          <Link to={`/listing/${property.id}`} className="view-btn">
            View Details
          </Link>

        </div>

      </div>

    </div>
  );
}

export default PropertyCard;
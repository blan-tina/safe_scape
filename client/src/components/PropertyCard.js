import "./PropertyCard.css";

function PropertyCard({ property }) {
  return (
    <div className="property-card">

      <div className="image-container">

        <img
          src={property.images?.[0]}
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
            ⭐ 4.9
          </span>
        </div>

        <p className="location">
          📍 {property.town}, {property.county}
        </p>

        <p className="details">
          🛏 {property.bedrooms} Bedrooms • 🚿 {property.bathrooms} Bathrooms
        </p>

        <p className="amenities">
          {property.amenities?.join(" • ")}
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

          <button className="view-btn">
            View
          </button>

        </div>

      </div>

    </div>
  );
}

export default PropertyCard;
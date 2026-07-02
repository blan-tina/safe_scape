import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

import "./PropertyDetails.css";

function PropertyDetails() {
  const { id } = useParams();

  const [property, setProperty] = useState(null);

  useEffect(() => {
    api
      .get(`/listings/${id}`)
      .then((res) => {
        setProperty(res.data);
      })
      .catch((err) => console.log(err));
  }, [id]);

  if (!property) {
    return <h1>Loading...</h1>;
  }

  return (
    <div className="property-details">

      <h1 className="property-title">
        {property.title}
      </h1>

      <p className="property-location">
        📍 {property.town}, {property.county}
      </p>

      <img
        src={property.images[0]}
        alt={property.title}
        className="hero-image"
      />

      <div className="property-content">

        <div className="left-column">

          <h2>About this property</h2>

          <p>{property.description}</p>

          <div className="features">

            <span>🛏 {property.bedrooms} Bedrooms</span>

            <span>🚿 {property.bathrooms} Bathrooms</span>

            <span>👨‍👩‍👧 {property.max_guests} Guests</span>

          </div>

          <h2>Amenities</h2>

          <div className="amenities">

            {property.amenities.map((amenity, index) => (
              <div className="amenity" key={index}>
                ✔ {amenity}
              </div>
            ))}

          </div>

          <h2 style={{marginTop:"50px"}}>
            Hosted by {property.host}
          </h2>

        </div>

        <div className="booking-card">

          <h2>
            KSh {property.price_per_night}
          </h2>

          <p>per night</p>

          <hr />

          <br />

          <label>Check In</label>

          <input
            type="date"
            style={{width:"100%",padding:"10px",marginBottom:"15px"}}
          />

          <label>Check Out</label>

          <input
            type="date"
            style={{width:"100%",padding:"10px"}}
          />

          <button className="reserve-btn">
            Reserve
          </button>

        </div>

      </div>

    </div>
  );
}

export default PropertyDetails;
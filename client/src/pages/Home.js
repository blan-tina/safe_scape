import { useEffect, useState } from "react";
import api from "../services/api";

import PropertyCard from "../components/PropertyCard";
import SearchBar from "../components/SearchBar";

function Home() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/listings")
      .then((response) => {
        setProperties(response.data);
      })
      .catch((error) => {
        console.error("Error fetching listings:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <h1>Find Your Next Safe Stay</h1>

        <p>
          Discover verified accommodation across Kenya.
        </p>
      </section>

      {/* Search Bar */}
      <SearchBar />

      {/* Property Listings */}
      <section className="properties">
        <h2>Featured Properties</h2>

        {loading ? (
          <p>Loading properties...</p>
        ) : properties.length > 0 ? (
          <div className="property-grid">
            {properties.map((property) => (
              <PropertyCard
                key={property.id}
                property={property}
              />
            ))}
          </div>
        ) : (
          <p>No properties available yet.</p>
        )}
      </section>
    </>
  );
}

export default Home;
import { useEffect, useState } from "react";
import api from "../services/api";

import PropertyCard from "../components/PropertyCard";
import SearchBar from "../components/SearchBar";

function Home() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState(null);

  useEffect(() => {
    const params = {};

    if (filters?.location) {
      params.location = filters.location;
    }

    if (filters?.checkIn && filters?.checkOut) {
      params.check_in = filters.checkIn;
      params.check_out = filters.checkOut;
    }

    if (filters?.guests) {
      params.guests = filters.guests;
    }

    setLoading(true);

    api
      .get("/listings", { params })
      .then((response) => {
        setProperties(response.data);
      })
      .catch((error) => {
        console.error("Error fetching listings:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [filters]);

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
      <SearchBar onSearch={setFilters} />

      {/* Property Listings */}
      <section className="properties">
        <h2>
          {filters?.location || filters?.checkIn
            ? "Search Results"
            : "Featured Properties"}
        </h2>

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
          <p>No properties match your search. Try adjusting your filters.</p>
        )}
      </section>
    </>
  );
}

export default Home;

import { useState } from "react";

import "./SearchBar.css";

function SearchBar({ onSearch }) {

  const [location, setLocation] = useState("");
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState("1");
  const [error, setError] = useState("");

  function handleSearch() {

    setError("");

    if ((checkIn && !checkOut) || (!checkIn && checkOut)) {
      setError("Please select both a check-in and check-out date.");
      return;
    }

    if (checkIn && checkOut && checkOut <= checkIn) {
      setError("Check-out date must be after check-in date.");
      return;
    }

    onSearch({
      location: location.trim(),
      checkIn,
      checkOut,
      guests,
    });
  }

  function handleClear() {
    setLocation("");
    setCheckIn("");
    setCheckOut("");
    setGuests("1");
    setError("");
    onSearch({ location: "", checkIn: "", checkOut: "", guests: "1" });
  }

  return (
    <div className="search-wrapper">

      <div className="search-box">

        <div className="search-item">
          <label>Where</label>
          <input
            type="text"
            placeholder="Search destination"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Check In</label>
          <input
            type="date"
            value={checkIn}
            onChange={(e) => setCheckIn(e.target.value)}
          />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Check Out</label>
          <input
            type="date"
            value={checkOut}
            onChange={(e) => setCheckOut(e.target.value)}
          />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Guests</label>

          <select
            value={guests}
            onChange={(e) => setGuests(e.target.value)}
          >
            <option value="1">1 Guest</option>
            <option value="2">2 Guests</option>
            <option value="3">3 Guests</option>
            <option value="4">4 Guests</option>
            <option value="5">5+ Guests</option>
          </select>
        </div>

        <button className="search-btn" onClick={handleSearch}>
          🔍 Search
        </button>

        {(location || checkIn || checkOut || guests !== "1") && (
          <button className="clear-btn" onClick={handleClear}>
            Clear
          </button>
        )}

      </div>

      {error && (
        <p className="search-error">
          {error}
        </p>
      )}

    </div>
  );
}

export default SearchBar;

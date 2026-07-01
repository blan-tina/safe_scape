import "./SearchBar.css";

function SearchBar() {
  return (
    <div className="search-wrapper">

      <div className="search-box">

        <div className="search-item">
          <label>Where</label>
          <input
            type="text"
            placeholder="Search destination"
          />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Check In</label>
          <input type="date" />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Check Out</label>
          <input type="date" />
        </div>

        <div className="divider"></div>

        <div className="search-item">
          <label>Guests</label>

          <select>
            <option>1 Guest</option>
            <option>2 Guests</option>
            <option>3 Guests</option>
            <option>4 Guests</option>
            <option>5+ Guests</option>
          </select>
        </div>

        <button className="search-btn">
          🔍 Search
        </button>

      </div>

    </div>
  );
}

export default SearchBar;
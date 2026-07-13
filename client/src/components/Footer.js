import { Link } from "react-router-dom";

import "./Footer.css";

function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">

      <div className="footer-content">

        <div className="footer-column">
          <h3 className="footer-logo">🛡 SafeScape</h3>
          <p>
            Find and book verified, safe accommodation across Kenya —
            from city apartments to beachfront villas.
          </p>
        </div>

        <div className="footer-column">
          <h4>Explore</h4>
          <Link to="/">Home</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </div>

        <div className="footer-column">
          <h4>Support</h4>
          <a href="mailto:support@safescape.com">Contact Us</a>
          <a href="#!">Help Center</a>
          <a href="#!">Safety Guidelines</a>
        </div>

        <div className="footer-column">
          <h4>Legal</h4>
          <a href="#!">Terms of Service</a>
          <a href="#!">Privacy Policy</a>
        </div>

      </div>

      <div className="footer-bottom">
        © {year} SafeScape. All rights reserved.
      </div>

    </footer>
  );
}

export default Footer;

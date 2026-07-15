# SafeScape

SafeScape is a full-stack bed & breakfast booking platform. Hosts can list
properties; guests can search, book, message hosts, and leave reviews.

Built with a **React** frontend and a **Flask + MySQL** backend, connected
by a JWT-authenticated REST API.

---

## ✨ Features

- **Authentication** — register/login as a guest or host, JWT-based sessions
- **Property listings** — hosts can create, edit, and delete properties with
  images and amenities
- **Search** — filter properties by destination, guest count, and date
  availability
- **Bookings** — guests can book available properties; hosts can accept or
  cancel pending bookings
- **Reviews** — guests who have booked a property can leave a rating and
  comment
- **Messaging** — guests and hosts can message each other about a property,
  with a full inbox/conversation view
- **Dashboards** — separate host and guest dashboards for managing
  properties, bookings, and messages

---

## 🧱 Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Frontend   | React, React Router, Axios          |
| Backend    | Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS |
| Database   | MySQL (via PyMySQL)                 |
| Auth       | JWT (JSON Web Tokens)               |

---

## 📁 Project Structure

```
Safe_scape/
├── client/          # React frontend
│   └── src/
│       ├── components/   # Navbar, Footer, PropertyCard, SearchBar...
│       ├── pages/         # Home, Login, Register, Dashboards, etc.
│       ├── context/       # AuthContext (login state)
│       ├── routes/        # ProtectedRoute
│       └── services/      # api.js (Axios instance)
└── server/          # Flask backend
    ├── app.py        # All API routes
    ├── models.py      # SQLAlchemy models
    ├── config.py      # Config (reads from .env)
    ├── seed.py        # Sample data for local development
    └── create_tables.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (project has been run on 3.8, but newer is recommended)
- Node.js 18+
- A running MySQL server

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Safe_scape.git
cd Safe_scape
```

### 2. Backend setup

```bash
cd server
pip install -r requirements.txt
```

Create a `server/.env` file (this is **not** committed to git — you must
create it yourself):

```
DATABASE_URL=mysql+pymysql://<db_user>:<db_password>@localhost/bnb_db
JWT_SECRET_KEY=some-long-random-secret
```

Create the database tables, then optionally load sample data:

```bash
python create_tables.py
python seed.py          # optional — adds demo properties, users, bookings
```

Run the server:

```bash
python app.py
```

The API will be running at `http://localhost:5000`.

### 3. Frontend setup

```bash
cd client
npm install
npm start
```

The app will be running at `http://localhost:3000`.

### Demo accounts (if you ran `seed.py`)

| Role  | Email                 | Password |
|-------|------------------------|----------|
| Host  | host@safescape.com     | 123456   |
| Host  | grace@safescape.com    | 123456   |
| Guest | guest@safescape.com    | 123456   |
| Guest | brian@safescape.com    | 123456   |

---

## 🔌 API Overview

All authenticated routes expect an `Authorization: Bearer <token>` header,
obtained from `/login` or `/register`.

**Auth**
| Method | Route        | Description            |
|--------|-------------|--------------------------|
| POST   | `/register` | Create an account, returns a token |
| POST   | `/login`    | Log in, returns a token  |

**Listings**
| Method | Route                              | Auth required | Description |
|--------|-------------------------------------|---------------|-------------|
| GET    | `/listings`                         | No            | List all available properties (supports `?location=`, `?guests=`, `?check_in=`, `?check_out=`) |
| GET    | `/listings/<id>`                    | No            | Get one property's full details |
| GET    | `/my-listings`                      | Yes (host)    | Get the logged-in host's own properties |
| POST   | `/listings`                         | Yes (host)    | Create a property |
| PUT    | `/listings/<id>`                    | Yes (owner)   | Update a property |
| DELETE | `/listings/<id>`                    | Yes (owner)   | Delete a property |
| POST   | `/listings/<id>/images`             | Yes (owner)   | Add an image |
| DELETE | `/images/<id>`                      | Yes (owner)   | Remove an image |
| POST   | `/listings/<id>/amenities`          | Yes (owner)   | Add an amenity |
| DELETE | `/amenities/<id>`                   | Yes (owner)   | Remove an amenity |

**Bookings**
| Method | Route                        | Auth required     | Description |
|--------|-------------------------------|--------------------|-------------|
| POST   | `/bookings`                   | Yes (guest)        | Book a property |
| GET    | `/my-bookings`                | Yes (guest)        | Get the logged-in guest's bookings |
| GET    | `/host-bookings`               | Yes (host)         | Get bookings across all of the host's properties |
| PUT    | `/bookings/<id>`              | Yes (host, owner)  | Update booking status (`pending`/`confirmed`/`cancelled`) |
| PATCH  | `/bookings/<id>/cancel`        | Yes (guest, owner) | Guest cancels their own booking |
| DELETE | `/bookings/<id>`              | Yes (participant)  | Delete a booking record |

**Reviews**
| Method | Route                    | Auth required | Description |
|--------|----------------------------|---------------|-------------|
| POST   | `/reviews`                 | Yes (guest)   | Leave a review (must have booked the property) |
| GET    | `/reviews/<listing_id>`     | No            | Get all reviews for a property |

**Messages**
| Method | Route                             | Auth required | Description |
|--------|-------------------------------------|---------------|-------------|
| POST   | `/messages`                        | Yes           | Send a message |
| GET    | `/messages/<user1>/<user2>`         | Yes (participant) | Get a conversation thread |
| GET    | `/conversations`                    | Yes           | List all of the logged-in user's conversations |

---

## 🔒 Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash`.
- All write actions (creating/editing/deleting listings, bookings, reviews,
  messages) require a valid JWT and are checked against ownership —
  users can only modify their own data.
- `.env` (containing DB credentials and the JWT secret) is gitignored and
  must be created locally; it is never committed.

---

## 🗺 Roadmap / Known Limitations

- Images are added via URL rather than direct file upload.
- No payment integration — bookings are recorded but not paid for
  in-app.
- No automated tests yet.

---

## ☁️ Deployment

This app deploys cleanly across three free services: **Aiven** (MySQL
database), **Render** (Flask backend), and **Vercel** (React frontend).

### 1. Database — Aiven (free MySQL)

1. Sign up at [aiven.io](https://aiven.io) (no credit card required).
2. Create a new service → choose **MySQL** → select the **Free** plan.
3. Once it's running, open the service's **Overview** tab and copy the
   connection URI. It looks like:
   ```
   mysql://avnadmin:<password>@<host>:<port>/defaultdb?ssl-mode=REQUIRED
   ```
4. Change `mysql://` to `mysql+pymysql://` at the start — that's the
   `DATABASE_URL` you'll use in the next step.

### 2. Backend — Render

1. Push your code to GitHub if you haven't already.
2. Sign up at [render.com](https://render.com) and create a **New Web
   Service**, connecting your GitHub repo.
3. Set the **Root Directory** to `server`.
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `gunicorn app:app`
6. Under **Environment**, add these variables (see `server/.env.example`):
   - `DATABASE_URL` — the Aiven connection string from step 1
   - `JWT_SECRET_KEY` — any long random string
   - `FRONTEND_URL` — you'll fill this in after step 3, once you know your
     Vercel URL
7. Deploy. Once live, run the table setup once — Render's dashboard has a
   **Shell** tab where you can run:
   ```bash
   python create_tables.py
   python seed.py   # optional, adds demo data
   ```
8. Note your backend's live URL (something like
   `https://safescape-api.onrender.com`) — you'll need it next.

> Free Render web services spin down after 15 minutes of inactivity and
> take ~30–60 seconds to wake back up on the next request. Fine for a
> portfolio project; not ideal if you need instant, always-on responses.

### 3. Frontend — Vercel

1. Sign up at [vercel.com](https://vercel.com) and import your GitHub repo.
2. Set the **Root Directory** to `client`.
3. Framework preset: **Create React App** (should auto-detect).
4. Add an environment variable:
   - `REACT_APP_API_URL` = your Render backend URL from step 2 (no
     trailing slash)
5. Deploy. Note the live Vercel URL you're given.

### 4. Connect them

Go back to your Render backend's environment variables and set
`FRONTEND_URL` to your actual Vercel URL, then redeploy the backend so
CORS allows requests from it.

Your app is now live end-to-end 🎉

---

## 📄 License

This project was built for educational purposes.

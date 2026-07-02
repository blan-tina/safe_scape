import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import HostDashboard from "./pages/HostDashboard";
import GuestDashboard from "./pages/GuestDashboard";
import PropertyDetails from "./pages/PropertyDetails";
import ProtectedRoute from "./routes/ProtectedRoute";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
            path="/guest-dashboard"
            element={
            <ProtectedRoute role="guest">
              <GuestDashboard />
            </ProtectedRoute>
      }
/>

        <Route
        path="/host-dashboard"
  element={
     <ProtectedRoute role="host">
      <HostDashboard />
    </ProtectedRoute>
       }
/>
        <Route path="/listing/:id" element={<PropertyDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
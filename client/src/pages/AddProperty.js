import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

import "./AddProperty.css";

function AddProperty() {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({

        title: "",
        description: "",
        country: "Kenya",
        county: "",
        town: "",
        address: "",
        price_per_night: "",
        bedrooms: 1,
        bathrooms: 1,
        max_guests: 1,
        image_url: "",
        amenities: ""

    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function handleChange(e) {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        setError("");
        setLoading(true);

        try {

            // 1. Create the listing itself.
            // host_id is derived server-side from the logged-in user's token,
            // so we only need to send the property details here.
            const response = await api.post("/listings", {
                title: formData.title,
                description: formData.description,
                country: formData.country,
                county: formData.county,
                town: formData.town,
                address: formData.address,
                price_per_night: Number(formData.price_per_night),
                bedrooms: Number(formData.bedrooms),
                bathrooms: Number(formData.bathrooms),
                max_guests: Number(formData.max_guests),
            });

            const listingId = response.data.listing.id;

            // 2. Attach the main image, if one was provided.
            if (formData.image_url.trim()) {
                await api.post(`/listings/${listingId}/images`, {
                    image_url: formData.image_url.trim(),
                });
            }

            // 3. Attach amenities, if any were provided (comma-separated).
            const amenityNames = formData.amenities
                .split(",")
                .map((name) => name.trim())
                .filter((name) => name.length > 0);

            for (const name of amenityNames) {
                await api.post(`/listings/${listingId}/amenities`, { name });
            }

            alert("Property added successfully!");

            navigate("/host-dashboard");

        } catch (err) {

            console.log(err);

            setError(
                err.response?.data?.error ||
                "Unable to add property."
            );

        } finally {
            setLoading(false);
        }

    }

    return (

        <div className="add-property-page">

            <div className="add-property-card">

                <h1>Add New Property</h1>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        name="title"
                        placeholder="Property Title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />

                    <textarea
                        name="description"
                        placeholder="Property Description"
                        value={formData.description}
                        onChange={handleChange}
                        rows="5"
                        required
                    />

                    <input
                        type="text"
                        name="county"
                        placeholder="County"
                        value={formData.county}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="text"
                        name="town"
                        placeholder="Town"
                        value={formData.town}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="text"
                        name="address"
                        placeholder="Address"
                        value={formData.address}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="number"
                        name="price_per_night"
                        placeholder="Price Per Night"
                        value={formData.price_per_night}
                        onChange={handleChange}
                        min="1"
                        required
                    />

                    <input
                        type="number"
                        name="bedrooms"
                        placeholder="Bedrooms"
                        value={formData.bedrooms}
                        onChange={handleChange}
                        min="1"
                        required
                    />

                    <input
                        type="number"
                        name="bathrooms"
                        placeholder="Bathrooms"
                        value={formData.bathrooms}
                        onChange={handleChange}
                        min="1"
                        required
                    />

                    <input
                        type="number"
                        name="max_guests"
                        placeholder="Guests"
                        value={formData.max_guests}
                        onChange={handleChange}
                        min="1"
                        required
                    />

                    <input
                        type="text"
                        name="image_url"
                        placeholder="Main Image URL"
                        value={formData.image_url}
                        onChange={handleChange}
                    />

                    <textarea
                        name="amenities"
                        placeholder="Amenities (WiFi, Parking, Pool...)"
                        value={formData.amenities}
                        onChange={handleChange}
                        rows="4"
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Adding..." : "Add Property"}
                    </button>

                </form>

            </div>

        </div>

    );

}

export default AddProperty;

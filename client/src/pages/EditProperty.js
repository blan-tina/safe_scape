import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import api from "../services/api";

import "./AddProperty.css";

function EditProperty() {

    const { id } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        country: "",
        county: "",
        town: "",
        address: "",
        price_per_night: "",
        bedrooms: 1,
        bathrooms: 1,
        max_guests: 1,
        available: true,
    });

    const [images, setImages] = useState([]);
    const [amenities, setAmenities] = useState([]);

    const [newImageUrl, setNewImageUrl] = useState("");
    const [newAmenityName, setNewAmenityName] = useState("");

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function fetchListing() {
            try {
                const response = await api.get(`/listings/${id}`);
                const listing = response.data;

                setFormData({
                    title: listing.title,
                    description: listing.description,
                    country: listing.country,
                    county: listing.county,
                    town: listing.town,
                    address: listing.address,
                    price_per_night: listing.price_per_night,
                    bedrooms: listing.bedrooms,
                    bathrooms: listing.bathrooms,
                    max_guests: listing.max_guests,
                    available: listing.available,
                });

                setImages(listing.images || []);
                setAmenities(listing.amenities || []);
            } catch (err) {
                setError("Unable to load this property.");
            } finally {
                setLoading(false);
            }
        }

        fetchListing();
    }, [id]);

    function handleChange(e) {
        const { name, value, type, checked } = e.target;

        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        setError("");
        setSaving(true);

        try {
            await api.put(`/listings/${id}`, {
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
                available: formData.available,
            });

            alert("Property updated successfully!");
            navigate("/host-dashboard");
        } catch (err) {
            setError(
                err.response?.data?.error || "Unable to update property."
            );
        } finally {
            setSaving(false);
        }
    }

    async function handleAddImage() {
        if (!newImageUrl.trim()) return;

        try {
            const response = await api.post(`/listings/${id}/images`, {
                image_url: newImageUrl.trim(),
            });

            setImages([
                ...images,
                { id: response.data.image.id, image_url: newImageUrl.trim() },
            ]);
            setNewImageUrl("");
        } catch (err) {
            setError(err.response?.data?.error || "Unable to add image.");
        }
    }

    async function handleDeleteImage(imageId) {
        try {
            await api.delete(`/images/${imageId}`);
            setImages(images.filter((img) => img.id !== imageId));
        } catch (err) {
            setError(err.response?.data?.error || "Unable to remove image.");
        }
    }

    async function handleAddAmenity() {
        if (!newAmenityName.trim()) return;

        try {
            const response = await api.post(`/listings/${id}/amenities`, {
                name: newAmenityName.trim(),
            });

            setAmenities([
                ...amenities,
                { id: response.data.amenity.id, name: newAmenityName.trim() },
            ]);
            setNewAmenityName("");
        } catch (err) {
            setError(err.response?.data?.error || "Unable to add amenity.");
        }
    }

    async function handleDeleteAmenity(amenityId) {
        try {
            await api.delete(`/amenities/${amenityId}`);
            setAmenities(amenities.filter((a) => a.id !== amenityId));
        } catch (err) {
            setError(err.response?.data?.error || "Unable to remove amenity.");
        }
    }

    if (loading) {
        return (
            <div className="add-property-page">
                <p style={{ textAlign: "center", padding: "40px" }}>
                    Loading property...
                </p>
            </div>
        );
    }

    return (
        <div className="add-property-page">

            <div className="add-property-card">

                <h1>Edit Property</h1>

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

                    <label
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            margin: "10px 0 20px",
                        }}
                    >
                        <input
                            type="checkbox"
                            name="available"
                            checked={formData.available}
                            onChange={handleChange}
                            style={{ width: "auto" }}
                        />
                        Listed as available for booking
                    </label>

                    <button type="submit" disabled={saving}>
                        {saving ? "Saving..." : "Save Changes"}
                    </button>

                </form>

                <hr style={{ margin: "30px 0" }} />

                <h2>Images</h2>

                {images.map((img) => (
                    <div
                        key={img.id}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            marginBottom: "10px",
                        }}
                    >
                        <img
                            src={img.image_url}
                            alt="Property"
                            style={{
                                width: "70px",
                                height: "50px",
                                objectFit: "cover",
                                borderRadius: "6px",
                            }}
                        />
                        <span style={{ flex: 1, wordBreak: "break-all" }}>
                            {img.image_url}
                        </span>
                        <button
                            type="button"
                            className="btn-small"
                            onClick={() => handleDeleteImage(img.id)}
                        >
                            Remove
                        </button>
                    </div>
                ))}

                <div style={{ display: "flex", gap: "10px" }}>
                    <input
                        type="text"
                        placeholder="New image URL"
                        value={newImageUrl}
                        onChange={(e) => setNewImageUrl(e.target.value)}
                    />
                    <button type="button" className="btn-small" onClick={handleAddImage}>
                        Add Image
                    </button>
                </div>

                <hr style={{ margin: "30px 0" }} />

                <h2>Amenities</h2>

                {amenities.map((amenity) => (
                    <div
                        key={amenity.id}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            marginBottom: "10px",
                        }}
                    >
                        <span style={{ flex: 1 }}>{amenity.name}</span>
                        <button
                            type="button"
                            className="btn-small"
                            onClick={() => handleDeleteAmenity(amenity.id)}
                        >
                            Remove
                        </button>
                    </div>
                ))}

                <div style={{ display: "flex", gap: "10px" }}>
                    <input
                        type="text"
                        placeholder="New amenity (e.g. WiFi)"
                        value={newAmenityName}
                        onChange={(e) => setNewAmenityName(e.target.value)}
                    />
                    <button type="button" className="btn-small" onClick={handleAddAmenity}>
                        Add Amenity
                    </button>
                </div>

            </div>

        </div>
    );
}

export default EditProperty;

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

    function handleChange(e) {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            await api.post("/listings", formData);

            alert("Property added successfully!");

            navigate("/host-dashboard");

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.error ||
                "Unable to add property."
            );

        }

    }

    return (

        <div className="add-property-page">

            <div className="add-property-card">

                <h1>Add New Property</h1>

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
                        required
                    />

                    

                    <input
                            type="number"
                            name="bedrooms"
                            placeholder="Rooms"
                            value={formData.bedrooms}
                            onChange={handleChange}
                            required
                        />

            

                    <input
                            type="number"
                            name="max_guests"
                            placeholder="Guests"
                            value={formData.max_guests}
                            onChange={handleChange}
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

                    <button type="submit">
                        Add Property
                    </button>

                </form>

            </div>

        </div>

    );

}

export default AddProperty;
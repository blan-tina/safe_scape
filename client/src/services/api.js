import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:5000", 
});


api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    console.log("Token from localStorage:", token); // <-- ADD THIS
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    console.log("Request headers:", config.headers); // <-- ADD THIS
    return config;
});

export default api;
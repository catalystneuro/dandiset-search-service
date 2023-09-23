import axios from 'axios';

// Create a client to connect to the REST API
const apiClient = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 120000, // 120 seconds
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;

import React, { useState } from 'react';
import { AxiosError } from 'axios';
import { TextField, Button, Box, Snackbar, Alert } from '@mui/material';
import apiClient from '../clients/rest_client';

interface SearchBoxProps {
    onSearch: (query: string) => void;
    onResults: (results: string[]) => void;
}

const SearchBox: React.FC<SearchBoxProps> = ({ onSearch, onResults }) => {
    const [query, setQuery] = useState<string>('');
    const [snackbarMessage, setSnackbarMessage] = useState<string | null>(null);

    const handleSearch = async () => {
        onSearch(query);  // You can still use the onSearch prop if needed elsewhere.
        setSnackbarMessage('Searching relevant dandisets... Please wait.');
        try {
            const responses = await Promise.all([
                apiClient.post('/search', {
                    text: query,
                    method: 'simple',
                }),
                apiClient.post('/search', {
                    text: query,
                    method: 'keywords',
                }),
            ]);

            const results = responses.map(res => res.data.text);
            onResults(results);
            setSnackbarMessage('Results found successfully!');
        } catch (err) {
            const axiosError = err as AxiosError<{ detail: string }>;
            setSnackbarMessage(axiosError.response?.data?.detail || 'Something went wrong');
        }
    };

    return (
        <Box display="flex" flexDirection="column" alignItems="center" gap={1} paddingBottom={2}>
            <TextField
                multiline
                rows={3}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search..."
                variant="outlined"
                style={{ width: '100%' }}
            />
            <Button variant="contained" color="primary" onClick={handleSearch}>
                Search
            </Button>

            {/* Display the snackbar message */}
            <Snackbar
                open={!!snackbarMessage}
                autoHideDuration={20000}
                onClose={() => setSnackbarMessage(null)}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}  // This line sets the position
            >
                <Alert onClose={() => setSnackbarMessage(null)} severity={snackbarMessage === 'Something went wrong' ? 'error' : 'success'}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>

        </Box>
    );
}

export default SearchBox;

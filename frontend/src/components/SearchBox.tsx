import React, { useState } from 'react';
import { AxiosError } from 'axios';
import { TextField, Button, Box, Snackbar, Alert } from '@mui/material';


interface SearchBoxProps {
    onSearch: (query: string) => void;
    onResults1: (results: string) => void;
    onResults2: (results: string) => void;
}

const SearchBox: React.FC<SearchBoxProps> = ({ onSearch, onResults1, onResults2 }) => {
    const [query, setQuery] = useState<string>('');
    const [snackbarMessage, setSnackbarMessage] = useState<string | null>(null);

    const handleSearch = async () => {
        onSearch(query);
        setSnackbarMessage('Searching relevant dandisets... Please wait.');

        let results: string[] = ['', ''];

        const processStream = async (url: string, data: any, results_id: number) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const reader = response.body!.getReader();
            let decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                results[results_id] += decoder.decode(value);
                if (results_id === 1) onResults1(results[results_id]);
                else onResults2(results[results_id]);
            }
        };

        try {
            await Promise.all([
                processStream('http://localhost:8000/search', { text: query, method: 'simple', stream: true }, 1),
                processStream('http://localhost:8000/search', { text: query, method: 'keywords', stream: true }, 2),
            ]);

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

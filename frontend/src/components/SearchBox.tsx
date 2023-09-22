import React from 'react';
import { TextField, Button, Box } from '@mui/material';

interface SearchBoxProps {
    onSearch: (query: string) => void;
}

const SearchBox: React.FC<SearchBoxProps> = ({ onSearch }) => {
    const [query, setQuery] = React.useState('');

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
            <Button variant="contained" color="primary" onClick={() => onSearch(query)}>
                Search
            </Button>
        </Box>
    );
}

export default SearchBox;

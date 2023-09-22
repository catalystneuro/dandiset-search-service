import React from 'react';
import { TextField, Box } from '@mui/material';

const TallTextBoxes: React.FC = () => {
    return (
        <Box
            display="flex"
            justifyContent="center"
            gap={2}
            style={{ minHeight: '500px' }}
        >
            <TextField
                id="outlined-multiline-static-1"
                label="Response"
                multiline
                rows={20}
                InputLabelProps={{ shrink: true }}
                sx={{ width: '50%' }}
            />
            <TextField
                id="outlined-multiline-static-2"
                label="Response"
                multiline
                rows={20}
                InputLabelProps={{ shrink: true }}
                sx={{ width: '50%' }}
            />
        </Box>
    );
}

export default TallTextBoxes;

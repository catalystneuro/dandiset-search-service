import React from 'react';
import { TextField, Box, Button } from '@mui/material';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';

interface TallTextBoxesProps {
    results: string[];
}

const TallTextBoxes: React.FC<TallTextBoxesProps> = ({ results }) => {
    return (
        <Box
            display="flex"
            justifyContent="center"
            gap={2}
            style={{ minHeight: '500px' }}
        >
            <Box sx={{ width: '50%' }}>
                <TextField
                    id="outlined-multiline-static-1"
                    label="Response"
                    multiline
                    rows={20}
                    value={results[0]}
                    InputLabelProps={{ shrink: true }}
                    sx={{ width: '100%' }}
                />
                <Button
                    startIcon={<ThumbUpAltIcon />}
                    variant="outlined"
                    sx={{ marginTop: 1 }}
                >
                    Like
                </Button>
            </Box>

            <Box sx={{ width: '50%' }}>
                <TextField
                    id="outlined-multiline-static-2"
                    label="Response"
                    multiline
                    rows={20}
                    value={results[1]}
                    InputLabelProps={{ shrink: true }}
                    sx={{ width: '100%' }}
                />
                <Button
                    startIcon={<ThumbUpAltIcon />}
                    variant="outlined"
                    sx={{ marginTop: 1 }}
                >
                    Like
                </Button>
            </Box>
        </Box>
    );
}

export default TallTextBoxes;

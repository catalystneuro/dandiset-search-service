import React from 'react';
import { Box, Button } from '@mui/material';
import ReactMarkdown from 'react-markdown';
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
                <ReactMarkdown
                    className='markdown-component'
                >
                    {results[0]}
                </ReactMarkdown>
                <Button
                    startIcon={<ThumbUpAltIcon />}
                    variant="outlined"
                    sx={{ marginTop: 1 }}
                >
                    Like
                </Button>
            </Box>

            <Box sx={{ width: '50%' }}>
                <ReactMarkdown
                    className='markdown-component'
                >
                    {results[1]}
                </ReactMarkdown>
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

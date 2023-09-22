import React from 'react';
import { Box } from '@mui/material';
import logoSrc from '../assets/logo.svg';

const Logo: React.FC = () => {
    return (
        <Box display="flex" justifyContent="center">
            <img src={logoSrc} alt="Logo" style={{ height: "100px" }} />
        </Box>
    );
}

export default Logo;

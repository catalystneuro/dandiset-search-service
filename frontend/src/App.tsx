import React from 'react';
import { CssBaseline, Container, Typography, createTheme, ThemeProvider, Box } from '@mui/material';
import Logo from './components/Logo';
import SearchBox from './components/SearchBox';
import TallTextBoxes from './components/TallTextBoxes';

const theme = createTheme({
  typography: {
    fontFamily: "'Roboto', sans-serif !important",
  },
  palette: {
    primary: {
      main: '#333',
    },
    background: {
      default: '#d7d7d7',
    },
  },
});

function App() {
  const [results1, setResults1] = React.useState<string>('');
  const [results2, setResults2] = React.useState<string>('');

  const handleSearch = async (query: string) => {
    setResults1('Searching for relevant dandisets... please wait');
    setResults2('Searching for relevant dandisets... please wait');
    console.log('query: ', query);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        minHeight="100vh"
        justifyContent="flex-start"
        py={5}
        width="100%"
        sx={{
          paddingLeft: "0px",
          paddingRight: "0px",
          marginLeft: "0px",
          marginRight: "0px",
        }}
      >
        <Container
          // component="main"
          sx={{
            maxWidth: "1400px !important",
            paddingLeft: "0px",
            paddingRight: "0px",
            marginLeft: "0px",
            marginRight: "0px",
          }}
        >
          <Logo />
          <Typography variant="h6" style={{ marginTop: '20px', marginBottom: '20px', textAlign: 'center', fontSize: "27px" }}>
            Find Dandisets
          </Typography>
          <SearchBox onSearch={handleSearch} onResults1={setResults1} onResults2={setResults2} />
          <TallTextBoxes results={[results1, results2]} />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;

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
      >
        <Container component="main" maxWidth="md">
          <Logo />
          <Typography variant="h6" style={{ marginTop: '20px', marginBottom: '20px', textAlign: 'center', fontSize: "27px" }}>
            Find Dandisets
          </Typography>
          <SearchBox onSearch={(query) => console.log(`Searching for ${query}`)} />
          <TallTextBoxes />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;

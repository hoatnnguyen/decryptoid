import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import Cipher from './components/Cipher';

function App() {
  return (
    // <div className="App">
    //   <SignIn />
    // </div>
    <Router>
      <Routes>
        <Route exact path="/" element={<Cipher />} />
        <Route exact path="/login" element={<SignIn />} />
        <Route exact path="/signup" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;


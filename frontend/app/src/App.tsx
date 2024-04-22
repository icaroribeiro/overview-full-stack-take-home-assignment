import NavigationBar from "./components/NavigationBar";
import About from "./pages/About";
import Home from "./pages/Home";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ShowPredictions from "./pages/ShowPredictions";
import MakePrediction from "./pages/MakePrediction";

function App() {
  return (
    <div className="App">
      <Router>
        <NavigationBar></NavigationBar>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/make-prediction" element={<MakePrediction />} />
          <Route path="/show-predictions" element={<ShowPredictions />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

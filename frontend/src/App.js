import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import IntradayPrediction from "./components/IntradayPrediction";
import StockPrediction from "./components/StockPrediction";
import Header from "./components/Header";
import Featured from "./components/Featured";

const App = () => {
  return (
    <div>
      <Header></Header>
      <Router>
            <Routes>
                <Route path="/" element={<Featured />} />
                <Route path="/trends" element={<StockPrediction />} />
                <Route path="/intraday" element={<IntradayPrediction />} />
            </Routes>
      </Router>
    </div>
  );
};

export default App;

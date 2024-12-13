import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import IntradayPrediction from "./components/IntradayPrediction";
import StockPrediction from "./components/StockPrediction";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/intraday" element={<IntradayPrediction />} />
                <Route path="/trends" element={<StockPrediction />} />
            </Routes>
        </Router>
    );
}

export default App;

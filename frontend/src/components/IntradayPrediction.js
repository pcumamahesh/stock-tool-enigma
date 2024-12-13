import React, { useState } from "react";
import axios from "axios";

const IntradayPrediction = () => {
    const [ticker, setTicker] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleTickerChange = (e) => setTicker(e.target.value);

    const handlePredictClick = async () => {
        setLoading(true);
        setError(null);

        if (!ticker) {
            setError("Please enter a stock ticker.");
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post("/api/intraday/", { ticker });
            setPrediction(response.data);
        } catch (err) {
            setError("An error occurred while fetching intraday predictions.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Intraday Stock Prediction</h1>
            <div>
                <label>
                    Ticker:
                    <input
                        type="text"
                        value={ticker}
                        onChange={handleTickerChange}
                        placeholder="Enter Stock Ticker (e.g., RELIANCE.NS)"
                    />
                </label>
            </div>
            <button onClick={handlePredictClick} disabled={loading}>
                {loading ? "Loading..." : "Get Intraday Prediction"}
            </button>

            {error && <p>{error}</p>}

            {prediction && (
                <div>
                    <h3>Prediction Result</h3>
                    <p>Predicted Close Price: ₹{prediction.predicted_close}</p>
                    <p>Trend: {prediction.predicted_trend}</p>
                    <p>Confidence: {prediction.confidence}%</p>
                </div>
            )}
        </div>
    );
};

export default IntradayPrediction;
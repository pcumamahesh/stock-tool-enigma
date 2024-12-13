// src/components/StockPrediction.js

import React, { useState } from "react";
import axios from "axios";

const StockPrediction = () => {
  const [ticker, setTicker] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  const handleStartDateChange = (e) => {
    setStartDate(e.target.value);
  };

  const handleEndDateChange = (e) => {
    setEndDate(e.target.value);
  };

  const handlePredictClick = async () => {
    setLoading(true);
    setError(null);

    // Make sure all fields are filled out
    if (!ticker || !startDate || !endDate) {
      setError("Please provide ticker, start date, and end date.");
      setLoading(false);
      return;
    }

    try {
      // Send POST request to the Django API with the necessary data
      const response = await axios.post("/api/trends/", {
        ticker: ticker,
        start_date: startDate,
        end_date: endDate,
      });

      setPrediction(response.data);
    } catch (err) {
      setError("An error occurred while fetching the prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Stock Trend Prediction</h1>
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
      <div>
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={handleStartDateChange}
          />
        </label>
      </div>
      <div>
        <label>
          End Date:
          <input type="date" value={endDate} onChange={handleEndDateChange} />
        </label>
      </div>
      <button onClick={handlePredictClick} disabled={loading}>
        {loading ? "Loading..." : "Get Prediction"}
      </button>

      {error && <p>{error}</p>}

      {prediction && (
        <div>
          <h3>Prediction Result</h3>
          <p>Ticker: {prediction.ticker}</p>
          <p>Predicted Close Price: {prediction.predicted_close}</p>
          <p>Predicted Trend: {prediction.predicted_trend}</p>
          <p>Confidence: {prediction.confidence}%</p>
        </div>
      )}
    </div>
  );
};

export default StockPrediction;

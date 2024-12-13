import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Card Component
const StockCard = ({ company }) => {
  const { ticker, name, icon } = company; // Destructure company props
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStockData = async () => {
      setLoading(true);
      setError(null);
      try {
        const APIKEY = "NB4OdUc1sX1QAXVIAWXJ2dZudBTkw_gC"; // Replace with your API key
        const response = await axios.get(
          `https://api.polygon.io/v2/aggs/ticker/${ticker}/range/1/day/2023-01-01/2024-03-20?apiKey=${APIKEY}`
        );

        if (response.data.results) {
          const transformedData = {
            labels: response.data.results.map((item) =>
              new Date(item.t).toLocaleDateString()
            ),
            prices: response.data.results.map((item) => item.c), // Closing price
          };
          setStockData(transformedData);
        } else {
          throw new Error("No stock data available.");
        }
      } catch (err) {
        setError("Failed to fetch stock data.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStockData();
  }, [ticker]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  const chartData = {
    labels: stockData.labels,
    datasets: [
      {
        label: `Stock Price of ${name}`,
        data: stockData.prices,
        fill: false,
        backgroundColor: "rgba(75,192,192,1)",
        borderColor: "rgba(75,192,192,1)",
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: "top" },
      title: { display: true, text: `${name} Stock Prices` },
    },
  };

  return (
    <div style={styles.card}>
      {/* Header */}
      <div style={styles.header}>
        <img src={icon} alt={`${name} logo`} style={styles.logo} />
        <div>
          <h3>{name}</h3>
          <p>Latest Price: ${stockData.prices[stockData.prices.length - 1]}</p>
        </div>
      </div>

      {/* Graph */}
      <div style={styles.graphContainer}>
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

// Component Styles
const styles = {
  card: {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "16px",
    margin: "16px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    maxWidth: "600px",
    backgroundColor: "#fff",
  },
  header: {
    display: "flex",
    alignItems: "center",
    marginBottom: "16px",
  },
  logo: {
    height: "50px",
    width: "50px",
    marginRight: "16px",
  },
  graphContainer: {
    height: "300px",
  },
};

export default StockCard;

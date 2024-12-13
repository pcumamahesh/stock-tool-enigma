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
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StockGraph = ({ ticker = "AAPL" }) => {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Stock Price for ${ticker}`,
      },
    },
  };

  useEffect(() => {
    const fetchStockData = async () => {
      setLoading(true);
      try {
        // Using the Polygon.io Aggregates (Bars) API endpoint
        const APIKEY = 'NB4OdUc1sX1QAXVIAWXJ2dZudBTkw_gC';
        const multiplier = 1;
        const timespan = 'day';
        const from = '2023-08-20';  // Adjust date range as needed
        const to = '2024-12-20';    // Adjust date range as needed

        const response = await axios.get(
          `https://api.polygon.io/v2/aggs/ticker/${ticker}/range/${multiplier}/${timespan}/${from}/${to}?apiKey=${APIKEY}`
        );

        if (response.data.results) {
          // Transform the data into the format needed for the chart
          const transformedData = {
            history: response.data.results.map(item => ({
              date: new Date(item.t).toLocaleDateString(),
              price: item.c  // closing price
            }))
          };
          setStockData(transformedData);
        }
      } catch (error) {
        console.error("Error fetching stock data:", error);
        // Set some dummy data for testing
        setStockData({
          history: [
            { date: '2024-03-01', price: 100 },
            { date: '2024-03-02', price: 105 },
            { date: '2024-03-03', price: 103 },
            { date: '2024-03-04', price: 107 },
            { date: '2024-03-05', price: 110 },
          ]
        });
      } finally {
        setLoading(false);
      }
    };

    fetchStockData();
  }, [ticker]);

  if (loading) {
    return <p>Loading...</p>;
  }

  const data = {
    labels: stockData?.history?.map(entry => entry.date) || [],
    datasets: [
      {
        label: `Stock Price (${ticker})`,
        data: stockData?.history?.map(entry => entry.price) || [],
        fill: false,
        backgroundColor: 'rgba(75,192,192,1)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 1
      }
    ]
  };

  return (
    <div style={{ height: '400px', width: '50%',backgroundColor:'rgb(0,0,0,0.1)', borderRadius:'5px' }}>
      <Line 
        key={`${ticker}-${JSON.stringify(data)}`} 
        options={options} 
        data={data} 
      />
    </div>
  );
};

export default StockGraph;

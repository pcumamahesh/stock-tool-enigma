import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const ComparisonGraph = () => {
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [actualData, setActualData] = useState(null);
  const [predictedData, setPredictedData] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateMonthlyIntervals = (start, end) => {
    const dates = [];
    let currentDate = new Date(start);
    const endDate = new Date(end);

    while (currentDate <= endDate) {
      dates.push(new Date(currentDate));
      currentDate.setMonth(currentDate.getMonth() + 2);
    }
    return dates;
  };

  const handleFetchData = async () => {
    setLoading(true);
    try {
      // Format ticker for Polygon API
      const polygonTicker = ticker.split('.')[0];

      // Fetch actual data from Polygon.io
      const actualResponse = await axios.get(`https://api.polygon.io/v2/aggs/ticker/${polygonTicker}/range/1/day/${startDate}/${endDate}?apiKey=NB4OdUc1sX1QAXVIAWXJ2dZudBTkw_gC`);
      const actualResults = actualResponse.data.results.map(item => ({
        date: new Date(item.t).toLocaleDateString(),
        price: item.c
      }));
      setActualData(actualResults);

      // Generate monthly intervals
      const dateIntervals = generateMonthlyIntervals(startDate, endDate);

      // Fetch predicted data for each interval sequentially
      const predictions = [];
      for (let i = 0; i < dateIntervals.length - 1; i++) {
        const newStartDate = dateIntervals[i].toISOString().split('T')[0];
        const newEndDate = dateIntervals[i + 1].toISOString().split('T')[0];

        try {
          const predictedResponse = await axios.get('/api/trends/', {
            params: { ticker, start_date: newStartDate, end_date: newEndDate }
          });

          // Assuming the response is a single object, not an array
          const { predicted_close, ticker: date } = predictedResponse.data;
          predictions.push({ date, price: predicted_close });
        } catch (error) {
          console.error(`Error fetching predicted data for interval ${newStartDate} to ${newEndDate}:`, error);
        }
      }
      setPredictedData(predictions);
    } catch (error) {
      console.error('Error fetching actual data:', error);
    } finally {
      setLoading(false);
    }
  };

  const data = {
    labels: actualData?.map(entry => entry.date) || [],
    datasets: [
      {
        label: 'Actual Data',
        data: actualData?.map(entry => entry.price) || [],
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
      {
        label: 'Predicted Data',
        data: predictedData?.map(entry => entry.price) || [],
        borderColor: 'rgba(255,99,132,1)',
        fill: false,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: `Comparison for ${ticker}` },
    },
    animation: {
      duration: 1000,
      easing: 'easeInOutQuad'
    }
  };

  return (
    <div>
      <form onSubmit={(e) => { e.preventDefault(); handleFetchData(); }}>
        <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value)} placeholder="Ticker (e.g., TCS.NS)" required />
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
        <button type="submit" disabled={loading}>{loading ? 'Loading...' : 'Fetch Data'}</button>
      </form>
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
        <div style={{ width: '45%' }}>
          <Line data={data} options={options} />
        </div>
      </div>
    </div>
  );
};

export default ComparisonGraph; 
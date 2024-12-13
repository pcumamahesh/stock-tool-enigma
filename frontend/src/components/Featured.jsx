import React from 'react'
import TrendCard from './TrendCard'
import '../styles/Featured.css'
import { useState, useEffect } from "react";
import axios from "axios";
function Featured() {

    const companies = [
        { ticker: "RELIANCE.NS", name: "Reliance", icon: "https://w7.pngwing.com/pngs/63/125/png-transparent-reliance-industries-jamnagar-reliance-communications-business-industry-reliance-angle-logo-business.png" },
        { ticker: "TCS.NS", name: "TCS", icon: "https://www.siegelgale.com/app/uploads/2021/10/SGCOM_Blog_211018.png" },
        { ticker: "INFY.NS", name: "Infosys", icon: "https://i.pinimg.com/736x/89/0c/25/890c250fe129488a586b1a99e8b68107.jpg" },
      ];
    
      const [data, setData] = useState([]);
      const [loading, setLoading] = useState(true);
      const [error, setError] = useState(null);
    
      useEffect(() => {
        const fetchStockPredictions = async () => {
          setLoading(true);
          setError(null);
    
          try {
            const responses = await Promise.all(
              companies.map((company) =>
                axios.post("/api/trends/", {
                  ticker: company.ticker,
                  start_date: "2022-01-01", 
                  end_date: "2024-12-31",
                })
              )
            );
    
            // Combine fetched data with company details
            const updatedData = responses.map((response, index) => ({
              ...companies[index],
              price: response.data.predicted_close,
              trend: response.data.predicted_trend,
            }));
    
            setData(updatedData);
          } catch (err) {
            setError("Failed to fetch stock predictions.");
          } finally {
            setLoading(false);
          }
        };
    
        fetchStockPredictions();
      }, []);

    return (
        <div>
      <h1>Stock Prediction Dashboard</h1>
      {loading && <p>Loading stock predictions...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ display: "flex", gap: "16px", justifyContent: "center", flexWrap: "wrap" }}>
        {!loading &&
          data.map((company) => (
            <TrendCard
              key={company.ticker}
              icon={company.icon}
              name={company.name}
              price={company.price ? `$${company.price}` : "N/A"}
              trend={company.trend || "Neutral"}
            />
          ))}
      </div>
    </div>
        
        // if not able to fetch or api not working then just use the below hard coded components
        
        
        // <div className='parent'>
        //     <h1>Featured</h1>
        //     <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '20px' }}>
        //         <TrendCard
        //             icon="https://example.com/company-icon1.png"
        //             name="Company A"
        //             price="123.45"
        //             trend="Uptrend"
        //         />
        //         <TrendCard
        //             icon="https://example.com/company-icon2.png"
        //             name="Company B"
        //             price="98.76"
        //             trend="Downtrend"
        //         />
        //         <TrendCard
        //             icon="https://example.com/company-icon3.png"
        //             name="Company C"
        //             price="150.00"
        //             trend="Neutral"
        //         />
        //     </div>
        // </div>
    )
}

export default Featured
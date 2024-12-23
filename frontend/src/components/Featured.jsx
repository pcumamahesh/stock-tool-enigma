import React from 'react'
import TrendCard from './TrendCard'
import Header from "./Header";
import '../styles/Featured.css'
import { useState, useEffect } from "react";
import axios from "axios";
// function Featured() {


const companies = [
    { ticker: "RELIANCE.NS", name: "Reliance", icon: "https://example.com/reliance-icon.png" },
    { ticker: "TCS", name: "TCS", icon: "https://example.com/tcs-icon.png" },
    { ticker: "INFY.NS", name: "Infosys", icon: "https://example.com/infosys-icon.png" },
];

const Featured = () => {
    const [data, setData] = useState([]); // State to store fetched data
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStockPredictions = async () => {
            setLoading(true);
            setError(null);

            try {
                const responses = await Promise.allSettled(
                    companies.map((company) =>
                        axios.get("/api/trends/", {
                            params: {
                                ticker: company.ticker,
                                start_date: "2023-01-01",
                                end_date: "2024-12-31",
                                interval: "1d",
                            },
                        })
                    )
                );

                // Process responses to handle success and failures
                const updatedData = responses.map((result, index) => {
                    if (result.status === "fulfilled") {
                        return {
                            ...companies[index],
                            price: result.value.data.predicted_close,
                            trend: result.value.data.predicted_trend,
                        };
                    } else {
                        return {
                            ...companies[index],
                            price: "N/A", // Fallback value
                            trend: "Error fetching data", // Error fallback
                        };
                    }
                });

                setData(updatedData);
            } catch (err) {
                console.error(err);
                setError("Failed to fetch stock predictions.");
            } finally {
                setLoading(false);
            }
        };

        fetchStockPredictions();
    }, []);

    if (loading) return<>  <Header></Header><div className='main'>Loading...</div>;</> 
    if (error) return <>  <Header></Header><div className='main'>{error}</div>;</>

    return (<>
        <Header></Header>
        <div className='main'>
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
    </>
    



        // <div className='parent'>
        //     <h1>Featured</h1>
        //     <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '20px' }}>
        //         <TrendCard
        //             icon="https://w7.pngwing.com/pngs/63/125/png-transparent-reliance-industries-jamnagar-reliance-communications-business-industry-reliance-angle-logo-business.png"
        //             name="Company A"
        //             price="123.45"
        //             trend="Uptrend"
        //         />
        //         <TrendCard
        //             icon="https://www.siegelgale.com/app/uploads/2021/10/SGCOM_Blog_211018.png"
        //             name="Company B"
        //             price="98.76"
        //             trend="Downtrend"
        //         />
        //         <TrendCard
        //             icon="https://i.pinimg.com/736x/89/0c/25/890c250fe129488a586b1a99e8b68107.jpg"
        //             name="Company C"
        //             price="150.00"
        //             trend="Neutral"
        //         />
        //     </div>
        // </div>
    )
}

export default Featured
import React from 'react';
import StockGraph from './StockGraph';
import '../styles/HomeComponent.css';

const HomeComponent = ({ companyLogo, companyName, stockPrice, ticker }) => {
    return (
        <div className="home-container">
            <div className="company-header">
                <img src={companyLogo} alt={`${companyName} logo`} className="company-logo" />
                <div className="company-info">
                    <h2>{companyName}</h2>
                    <p className="stock-price">${stockPrice}</p>
                </div>
            </div>
            <div className="graph-container">
                <StockGraph ticker={ticker} />
            </div>
        </div>
    );
};

export default HomeComponent; 
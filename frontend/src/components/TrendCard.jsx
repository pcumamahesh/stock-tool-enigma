import React from "react";
import "../styles/TrendCard.css"; 

const TrendCard = ({ icon, name, price, trend }) => {
  return (
    <div className="trend-card">
        <div className="company-info">

      <img src={icon} alt={`${name} Icon`} className="trend-card-icon" />
      <h2 className="trend-card-name">{name}</h2>
        </div>
      <p className="trend-card-price">{price}</p>
      <p
        className={`trend-card-status ${
          trend.toLowerCase() === "uptrend"
            ? "uptrend"
            : trend.toLowerCase() === "downtrend"
            ? "downtrend"
            : "neutral"
        }`}
      >
        {trend === "Uptrend" ? "📈" : trend === "Downtrend" ? "📉" : "📊"} {trend}
      </p>
    </div>
  );
};

export default TrendCard;

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import IntradayPrediction from "./components/IntradayPrediction";
import StockPrediction from "./components/StockPrediction";

import Featured from "./components/Featured";
import StockGraph from "./components/StockGraph";
import HomeComponent from "./components/HomeComponent";
import StockCard from "./components/StockCard";
import "./App.css";

const App = () => {
  ;
  return (
    <> 
      <div className="page-1">
        <Featured></Featured>
      </div>
      <div className="page-2">
        <HomeComponent 
          companyLogo="https://www.siegelgale.com/app/uploads/2021/10/SGCOM_Blog_211018.png"
          companyName="TCS"
          stockPrice="3500.00"
          ticker="TCS"
        />
        
      </div>
    </>
  );
  
  
};

export default App;

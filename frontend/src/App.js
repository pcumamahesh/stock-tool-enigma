// src/App.js

import React from "react";
import StockPrediction from "./components/StockPrediction";
import Header from "./components/Header";
import Featured from "./components/Featured";

const App = () => {
  return (
    <div>
      <Header></Header>
      <Featured></Featured>
      
      {/* <StockPrediction /> */}

    </div>
  );
};

export default App;

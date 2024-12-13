// src/App.js

import React from "react";
import StockPrediction from "./components/StockPrediction";
import Header from "./components/Header";
import Featured from "./components/Featured";

const App = () => {
  return (
    <> 
    <Header></Header>
    <div>
      <Featured></Featured>
      
      {/* <StockPrediction /> */}

    </div>
    </>
  );
};

export default App;

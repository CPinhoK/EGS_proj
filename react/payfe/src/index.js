import React from 'react';
import * as ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import GetWallet from './GetWallet';
import PutWallet from './PutWallet';
import Transfer from './Transfer';
import GetPaymentHist from './GetPaymentHist';
import DeleteWallet from './DeleteWallet';

import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';


import {
  Navigation,
  Home,
} from "./components";


const rootNode=document.getElementById('root');

ReactDOM.createRoot(rootNode).render(
  <BrowserRouter>
    <Navigation />
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/CreateWallet" element={<App />} />
      <Route path="/GetWallet" element={<GetWallet />} />
      <Route path="/PutWallet" element={<PutWallet />} />
      <Route path="/TransferCash" element={<Transfer />} />
      <Route path="/PaymentHist" element={<GetPaymentHist />} />
      <Route path="/DeleteWallet" element={<DeleteWallet />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
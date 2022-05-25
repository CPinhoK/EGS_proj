import React from 'react';
import * as ReactDOM from 'react-dom/client';
import './index.css';
import CreateWallet from './CreateWallet';
import GetWallet from './GetWallet';
import PutWallet from './PutWallet';
import Transfer from './Transfer';
import GetPaymentHist from './GetPaymentHist';
import DeleteWallet from './DeleteWallet';
import Payment from './Payment';
import Login from './Login';

import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import ProtectedRoutes from './components/ProtectedRoutes';

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
      <Route path="/create-wallet" element={<CreateWallet />} />
      <Route path="/get-wallet" element={<GetWallet />} />
      <Route path="/alter-wallet" element={<PutWallet />} />
      <Route path="/money-transfer" element={<Transfer />} />
      <Route path="/transaction-history" element={<GetPaymentHist />} />
      <Route path="/delete-wallet" element={<DeleteWallet />} />
      <Route element={<ProtectedRoutes />}>
        <Route path="/payment" element={<Payment />} />
      </Route>
      <Route path="/params/*" element={<Login />} />
      <Route path="*" element={<div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}} ><h1 >404 NOT FOUND</h1></div>} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals <Route path="/login" element={<Login />} />
reportWebVitals();
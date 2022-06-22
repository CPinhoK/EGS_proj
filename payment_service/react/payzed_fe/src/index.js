import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';

import CreateWallet from './CreateWallet';
import GetWallet from './GetWallet';
import PutWallet from './PutWallet';
import Transfer from './Transfer';
import GetPaymentHist from './GetPaymentHist';
import DeleteWallet from './DeleteWallet';
import Payment from './Payment';
import Login from './Login';
import Signup from './Signup';
import Logout from './Logout';
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
      <Route path="/signup" element={<Signup />} />
      <Route path="/logout" element={<Logout />} />
      <Route element={<ProtectedRoutes />}>
        <Route path="/payment" element={<Payment />} />
      </Route>
      <Route path="/params/*" element={<Login />} />
      <Route path="*" element={<div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}} ><h1 >404 NOT FOUND</h1></div>} />
    </Routes>
  </BrowserRouter>
);






// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorkerRegistration.unregister();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

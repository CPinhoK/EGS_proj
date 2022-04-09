import React from "react";
import { NavLink } from "react-router-dom";

function Navigation() {
  return (
    <div className="navigation">
      <nav className="navbar navbar-expand navbar-dark bg-dark">
        <div className="container">
          <NavLink className="navbar-brand" to="/">
            PAYZ
          </NavLink>
          <div>
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <NavLink className="nav-link" to="/">
                     Home
                  <span className="sr-only">(current)</span>
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/CreateWallet">
                    Create Wallet
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/GetWallet">
                    Wallet Info
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/PutWallet">
                    Update Wallet
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/TransferCash">
                    Transfer Cash
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/PaymentHist">
                    Payments History
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/DeleteWallet">
                    Delete Wallet
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Navigation;
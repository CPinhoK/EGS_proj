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
                <NavLink className="nav-link" to="/create-wallet">
                    Create Wallet
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/get-wallet">
                    Wallet Info
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/alter-wallet">
                    Update Wallet
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/money-transfer">
                    Transfer Cash
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/transaction-history">
                    Payments History
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/delete-wallet">
                    Delete Wallet
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/login">
                    LogIn
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
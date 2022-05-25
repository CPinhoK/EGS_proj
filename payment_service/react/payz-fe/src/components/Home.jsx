import React from "react";
import ewallet from "./ewallet.png"


export default class Home extends React.Component {
  render() {
    return (
          <div className="home">
          <div className="container">
            <div className="row align-items-center my-5">
    
              <div className="col-lg-5">
                <h1 className="font-weight-light">PAYZ</h1>
                <p>
                  WELCOME TO PAYZ A ONLINE WALLET SERVICE <br/><br/><br/> ON A NEW REGISTRATION 2$ WILL PUT IN YOUR WALLET :)  <br/> BE ADVISED A FLAT TAX OF 0.2$ IS APPLYED ON PAYMENT TRANSACTIONS <br/> ALL TRANSACTIONS BETWEEN WALLETS ARE FREE
                </p>
              </div>
              <img className="mycontainer2" src={ewallet} alt="ewallet" />
            </div>
          </div>
        </div>
    );
  }
}

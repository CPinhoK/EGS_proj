import { Navigate, Outlet } from "react-router-dom";
import { useCookies } from 'react-cookie';


var useAuth = () => {
  const [cookies] = useCookies(['auth'])
  console.log(cookies.auth)
  const user = { loggedIn: false };
  if(cookies.auth===null||cookies.auth===undefined){
    user.loggedIn=false;
  }
  else{
    user.loggedIn=true;
  }
  return user && user.loggedIn;
};

const ProtectedRoutes = () => {
  const isAuth = useAuth();
  console.log(isAuth)
  return isAuth ? <Outlet /> : <Navigate to="/" />;
};

export default ProtectedRoutes;

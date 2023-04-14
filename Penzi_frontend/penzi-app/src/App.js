import React, { useState } from 'react';
import Admin from './Admin';
import ChatApp from './ChatApp';
import Login from './Login';
import { Route, BrowserRouter as Router, Routes, Navigate} from 'react-router-dom';


const App = () => {

  const[phoneNumber, setPhoneNumber] = useState('');
  const chatAppElement = phoneNumber ? (
    <ChatApp phoneNumber={phoneNumber} />
  ) : (
    <Navigate to="/" replace />
  );

  return (
    <>
    
      <Routes>
        <Route exact path='/chat' element={chatAppElement}/>
        <Route path='/admin' element={<Admin/>}/>
        <Route exact path='/' element={ <Login setPhoneNumber={setPhoneNumber}/>}></Route>
      </Routes>

    </>
  );
}

export default App;

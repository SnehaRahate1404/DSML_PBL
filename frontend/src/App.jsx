import { useState } from 'react'
import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Landing from './component/Landing';
import './App.css'
import Characters from './component/Characters';
import Conversation from './component/Conversation';

function App() {


  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/characters" element={<Characters />} />
          {/* <Route path="/chatp" element={<Characters />} /> */}
          <Route path="/chatp?character={character}" element={<Conversation />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  )
}

export default App

// write page for speech to speech communication thier must be a button to start the conversation
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './conversation.css'; // Assuming you have a CSS file for styling
import { FaMicrophone, FaStop } from 'react-icons/fa';

const Conversation = () => {
    const location = useLocation();
    const characterName = new URLSearchParams(location.search).get('character');
    const [isRecording, setIsRecording] = useState(false);
    const [messages, setMessages] = useState([]);
    
    const handleStartRecording = () => {
        setIsRecording(true);
        // Logic to start speech recognition
    };
    
    const handleStopRecording = () => {
        setIsRecording(false);
        // Logic to stop speech recognition and process the input
    };
    
    return (
        <div className="conversation-container">
        <h1>Chat with {characterName}</h1>
        <div className="chat-box">
            {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
                {msg.text}
            </div>
            ))}
        </div>
        <div className="controls">
            <button onClick={handleStartRecording} disabled={isRecording}>
            <FaMicrophone /> Start Recording
            </button>
            <button onClick={handleStopRecording} disabled={!isRecording}>
            <FaStop /> Stop Recording
            </button>
        </div>
        </div>
    );
    }

export default Conversation;
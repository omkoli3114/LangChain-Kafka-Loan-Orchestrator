import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Paperclip, Bot, User, Loader2 } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const ChatInterface = () => {
    const [sessionId] = useState(() => `session-${Math.random().toString(36).substr(2, 9)}`);
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your Capital Connect assistant. May I have your phone number to verify your account?' }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        const userMessage = { role: 'user', content: inputText };
        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsLoading(true);

        try {
            const response = await axios.post(`${API_BASE_URL}/chat`, {
                session_id: sessionId,
                user_id: 'user-1', // Placeholder
                message: userMessage.content
            });

            const botMessage = { role: 'assistant', content: response.data.reply };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: "I'm having trouble connecting right now. Please try again." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', sessionId);

        setIsLoading(true);
        // Add a temporary message for upload
        setMessages(prev => [...prev, { role: 'user', content: `Uploading ${file.name}...` }]);

        try {
            const response = await axios.post(`${API_BASE_URL}/upload/salary_slip`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            // The backend returns an agent reply directly
            const botMessage = { role: 'assistant', content: response.data.agent_reply };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: "Failed to upload file." }]);
        } finally {
            setIsLoading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white shadow-xl rounded-lg overflow-hidden">
            {/* Header */}
            <div className="bg-blue-600 p-4 text-white flex items-center space-x-2">
                <Bot className="w-6 h-6" />
                <h1 className="text-xl font-bold">Capital Connect</h1>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-none'
                                    : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
                                }`}
                        >
                            <div className="flex items-center space-x-2 mb-1 opacity-70 text-xs">
                                {msg.role === 'user' ? <User size={12} /> : <Bot size={12} />}
                                <span>{msg.role === 'user' ? 'You' : 'Agent'}</span>
                            </div>
                            <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-gray-200 p-3 rounded-lg rounded-bl-none shadow-sm flex items-center space-x-2">
                            <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                            <span className="text-sm text-gray-500">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-200">
                <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
                    <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="p-2 text-gray-500 hover:text-blue-600 transition-colors"
                        title="Upload Salary Slip"
                    >
                        <Paperclip className="w-5 h-5" />
                    </button>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        className="hidden"
                        accept=".pdf,.png,.jpg,.jpeg"
                    />

                    <input
                        type="text"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />

                    <button
                        type="submit"
                        disabled={isLoading || !inputText.trim()}
                        className="p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;

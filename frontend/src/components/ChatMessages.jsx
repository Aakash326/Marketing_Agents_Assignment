import React, { useEffect, useRef } from 'react';
import DataVisualization from './DataVisualization';
import { User, Bot } from 'lucide-react';

const ChatMessages = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="h-full overflow-y-auto p-4 bg-white rounded-lg shadow">
      <div className="space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p className="text-lg">Ask me anything about your portfolio!</p>
            <p className="text-sm mt-2">Try: "What stocks do I own?" or "Show my best performers"</p>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className="space-y-2">
            {message.role === 'user' ? (
              <div className="flex justify-end">
                <div className="max-w-[80%]">
                  <div className="flex items-start gap-2 justify-end">
                    <div className="bg-blue-600 text-white rounded-lg px-4 py-3">
                      <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    </div>
                    <div className="bg-blue-100 rounded-full p-2">
                      <User className="w-5 h-5 text-blue-600" />
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex justify-start">
                <div className="max-w-[80%]">
                  <div className="flex items-start gap-2">
                    <div className="bg-gray-100 rounded-full p-2">
                      <Bot className="w-5 h-5 text-gray-600" />
                    </div>
                    <div className="bg-gray-100 rounded-lg px-4 py-3">
                      <p className="text-sm whitespace-pre-wrap text-gray-800">
                        {message.content}
                      </p>
                    </div>
                  </div>

                  {/* Render visualizations if available */}
                  {message.visualizationData && (
                    <div className="ml-12 mt-3">
                      <DataVisualization data={message.visualizationData} />
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatMessages;

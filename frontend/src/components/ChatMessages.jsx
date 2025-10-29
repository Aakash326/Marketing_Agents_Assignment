import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
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
                    <div className="bg-gray-100 rounded-lg px-4 py-3 prose prose-sm max-w-none">
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        className="text-gray-800"
                        components={{
                          // Custom styling for markdown elements
                          h1: ({node, ...props}) => <h1 className="text-xl font-bold mb-2" {...props} />,
                          h2: ({node, ...props}) => <h2 className="text-lg font-bold mb-2 mt-3" {...props} />,
                          h3: ({node, ...props}) => <h3 className="text-base font-semibold mb-1 mt-2" {...props} />,
                          p: ({node, ...props}) => <p className="mb-2" {...props} />,
                          ul: ({node, ...props}) => <ul className="list-disc ml-4 mb-2" {...props} />,
                          ol: ({node, ...props}) => <ol className="list-decimal ml-4 mb-2" {...props} />,
                          li: ({node, ...props}) => <li className="mb-1" {...props} />,
                          strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                          em: ({node, ...props}) => <em className="italic" {...props} />,
                          code: ({node, inline, ...props}) => 
                            inline ? 
                              <code className="bg-gray-200 px-1 py-0.5 rounded text-xs" {...props} /> :
                              <code className="block bg-gray-800 text-white p-2 rounded my-2 text-xs" {...props} />,
                          blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-blue-500 pl-3 italic my-2" {...props} />,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
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

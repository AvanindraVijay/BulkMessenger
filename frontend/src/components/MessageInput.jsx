import React from 'react';

const MessageInput = ({ message, setMessage, disabled }) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        📝 Your Message
      </label>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        disabled={disabled}
        placeholder="Type your message here..."
        className="w-full px-3 py-2 border border-gray-300 rounded-lg 
                  focus:outline-none focus:border-blue-500
                  disabled:bg-gray-100 disabled:cursor-not-allowed"
        rows="5"
        maxLength="1000"
      />
      <div className="mt-1 text-right text-sm text-gray-500">
        {message.length}/1000 characters
      </div>
    </div>
  );
};

export default MessageInput;
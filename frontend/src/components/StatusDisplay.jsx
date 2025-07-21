import React from 'react';

const StatusDisplay = ({ status }) => {
  const { type, message, contactsProcessed } = status;

  return (
    <div className={`p-4 rounded-lg border ${
      type === 'success' 
        ? 'bg-green-50 border-green-200 text-green-800' 
        : 'bg-red-50 border-red-200 text-red-800'
    }`}>
      <div className="flex items-start space-x-2">
        <span className="text-lg">
          {type === 'success' ? '✅' : '❌'}
        </span>
        <div>
          <p className="font-medium">{message}</p>
          {contactsProcessed && (
            <p className="text-sm mt-1">
              Contacts processed: {contactsProcessed}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default StatusDisplay;
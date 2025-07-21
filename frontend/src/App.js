import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import MessageInput from './components/MessageInput';
import StatusDisplay from './components/StatusDisplay';
import { sendBulkMessage } from './services/api';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file || !message.trim()) {
      setStatus({
        type: 'error',
        message: 'Please provide both a message and a file.'
      });
      return;
    }

    // Validate file type
    const allowedTypes = ['.csv', '.xlsx', '.xls', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(fileExtension)) {
      setStatus({
        type: 'error',
        message: 'Please upload a valid CSV, Excel, or TXT file.'
      });
      return;
    }

    setLoading(true);
    setStatus(null);

    try {
      const response = await sendBulkMessage(message, file);
      setStatus({
        type: 'success',
        message: response.message,
        contactsProcessed: response.contacts_processed
      });
    } catch (error) {
      setStatus({
        type: 'error',
        message: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setMessage('');
    setStatus(null);
    document.getElementById('file-input').value = '';
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            📱 WhatsApp Bulk Sender
          </h1>
          <p className="text-gray-600">
            Send messages to multiple contacts from CSV, Excel, or TXT files
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <MessageInput
              message={message}
              setMessage={setMessage}
              disabled={loading}
            />
            
            <FileUpload
              file={file}
              setFile={setFile}
              disabled={loading}
            />

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={loading || !file || !message.trim()}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 
                          text-white font-medium py-2 px-4 rounded-lg
                          disabled:cursor-not-allowed"
              >
                {loading ? 'Sending...' : '🚀 Send Messages'}
              </button>
              
              <button
                type="button"
                onClick={handleReset}
                disabled={loading}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 
                          hover:bg-gray-50 disabled:cursor-not-allowed"
              >
                Reset
              </button>
            </div>
          </form>

          {status && (
            <div className="mt-6">
              <StatusDisplay status={status} />
            </div>
          )}
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>⚠️ Make sure WhatsApp Web is logged in before sending</p>
          <p>📋 Supported formats:</p>
          <p>📊 TXT/CSV/Excel: Phone numbers in any column</p>
          <p>📄 TXT: One phone number per line</p>
        </div>
      </div>
    </div>
  );
}

export default App;
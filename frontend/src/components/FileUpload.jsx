import React from 'react';

const FileUpload = ({ file, setFile, disabled }) => {
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const removeFile = () => {
    setFile(null);
    // Reset the input
    document.getElementById('file-input').value = '';
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    switch (extension) {
      case 'csv':
        return '📊';
      case 'xlsx':
      case 'xls':
        return '📗';
      case 'txt':
        return '📄';
      default:
        return '📄';
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        📁 Select Contact File
      </label>
      
      {!file ? (
        <div>
          <input
            id="file-input"
            type="file"
            accept=".csv,.xlsx,.xls,.txt"
            onChange={handleFileChange}
            disabled={disabled}
            className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-lg file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100
                      disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <p className="mt-2 text-sm text-gray-500">
            Select CSV, Excel, or TXT file with phone numbers
          </p>
          <div className="mt-2 text-xs text-gray-400">
            <p>📊 CSV: Phone numbers in any column</p>
            <p>📗 Excel: Phone numbers in any column</p>
            <p>📄 TXT: One phone number per line</p>
          </div>
        </div>
      ) : (
        <div className="border border-gray-300 rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{getFileIcon(file.name)}</span>
              <div>
                <p className="font-medium text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={removeFile}
              disabled={disabled}
              className="text-red-600 hover:text-red-800 px-2 py-1 rounded
                        disabled:cursor-not-allowed disabled:opacity-50"
            >
              Remove
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
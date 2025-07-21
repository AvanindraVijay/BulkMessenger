import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const sendBulkMessage = async (message, file) => {
  try {
    const formData = new FormData();
    formData.append('message', message);
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/send-message`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.status === 'error') {
      throw new Error(response.data.message);
    }

    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message || 'Server error');
    }
    throw new Error('Cannot connect to server. Make sure backend is running.');
  }
};
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const analyzeSymptoms = async (symptoms) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, { symptoms });
    return response.data;
  } catch (error) {
    console.error("Error analyzing symptoms:", error);
    throw error;
  }
};

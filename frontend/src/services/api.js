import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const analyzeSymptoms = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, data);
    return response.data;
  } catch (error) {
    console.error("Error analyzing symptoms:", error);
    throw error;
  }
};

export const submitFollowup = async (responses) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/followup`, { question_responses: responses });
    return response.data;
  } catch (error) {
    console.error("Error submitting followup:", error);
    throw error;
  }
};

export const refineDiagnosis = async (analysisId, responses) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/refine-diagnosis`, {
      initial_analysis_id: analysisId,
      followup_responses: responses
    });
    return response.data;
  } catch (error) {
    console.error("Error refining diagnosis:", error);
    throw error;
  }
};

export const getReport = async (analysisId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/report/${analysisId}`);
    return response.data;
  } catch (error) {
    console.error("Error getting report:", error);
    throw error;
  }
};

import React, { useState } from 'react';
import SymptomInput from '../components/SymptomInput';
import DoctorSelection from '../components/DoctorSelection';
import DiagnosisCard from '../components/DiagnosisCard';
import TestRecommendations from '../components/TestRecommendations';
import MultiHospitalSection from '../components/MultiHospitalSection';
import { ConfidenceChart, DoctorChart, RiskTimeline, SymptomImpact, RiskMeter, ClinicalInsights } from '../components/VisualizationCharts';
import { analyzeSymptoms, submitFollowup, refineDiagnosis } from '../services/api';

export default function Dashboard() {
  const [symptoms, setSymptoms] = useState('');
  const [patientData, setPatientData] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [followUpQuestions, setFollowUpQuestions] = useState([]);
  const [followupFromAnalysis, setFollowupFromAnalysis] = useState([]);
  const [analysisId, setAnalysisId] = useState(null);
  const [doctorView, setDoctorView] = useState(false);

  // Helper function to safely extract string values from result objects
  const sanitizeResult = (data) => {
    if (!data) return {};
    
    return {
      diagnosis: typeof data.diagnosis === 'string' ? data.diagnosis : 'Unknown Diagnosis',
      confidence: typeof data.confidence === 'number' ? data.confidence : 0,
      risk: typeof data.risk === 'string' ? data.risk : 'Unknown',
      explanation: typeof data.explanation === 'string' ? data.explanation : 
                   (typeof data.explanation === 'object' && data.explanation?.key_factors ? data.explanation.key_factors : 'No explanation available'),
      patient_report: typeof data.patient_report === 'string' ? data.patient_report : '',
      doctor_opinions: Array.isArray(data.doctor_opinions) ? data.doctor_opinions : [],
      tests: Array.isArray(data.tests) ? data.tests : [],
      followup_questions: Array.isArray(data.followup_questions) ? data.followup_questions : []
    };
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    setFollowUpQuestions([]);
    setFollowupFromAnalysis([]);

    try {
      const data = await analyzeSymptoms({
        symptoms,
        ...patientData,
        generate_followup: true  // Request follow-up questions
      });

      if (data.status === 'error') {
        setError(data.message);
      } else if (data.status === 'emergency') {
        setError(data.message);
        // Could show emergency modal here
      } else if (data.status === 'follow_up') {
        setFollowUpQuestions(data.follow_up_questions || []);
      } else if (data.status === 'success') {
        const sanitized = sanitizeResult(data);
        setResult(sanitized);
        setAnalysisId(Date.now().toString()); // Simple ID for demo
        if (sanitized.followup_questions && sanitized.followup_questions.length > 0) {
          setFollowupFromAnalysis(sanitized.followup_questions);
        }
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError("Analysis failed. Please check if the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleRefineDiagnosis = async (responses) => {
    if (!analysisId) return;

    setLoading(true);
    setError('');

    try {
      const data = await refineDiagnosis(analysisId, responses);
      // Update result with refined diagnosis
      setResult(prev => ({
        ...prev,
        diagnosis: data.refined_diagnosis || prev.diagnosis,
        confidence: data.confidence_score || prev.confidence,
        risk: data.risk_assessment || prev.risk,
        explanation: data.key_factors || prev.explanation
      }));
      setFollowupFromAnalysis([]);
    } catch (err) {
      setError("Diagnosis refinement failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleFollowUpSubmit = async (responses) => {
    setLoading(true);
    setError('');

    try {
      // Update patient data with responses
      const updatedData = { ...patientData };
      Object.keys(responses).forEach(question => {
        if (question.toLowerCase().includes('age')) {
          updatedData.age = parseInt(responses[question]);
        } else if (question.toLowerCase().includes('gender')) {
          updatedData.gender = responses[question].toLowerCase();
        } else if (question.toLowerCase().includes('duration')) {
          updatedData.duration = responses[question];
        } else if (question.toLowerCase().includes('severity')) {
          updatedData.severity = responses[question].toLowerCase();
        }
      });
      setPatientData(updatedData);

      // Re-run analysis with complete data
      const data = await analyzeSymptoms({
        symptoms,
        ...updatedData,
        generate_followup: true
      });

      if (data.status === 'success') {
        const sanitized = sanitizeResult(data);
        setResult(sanitized);
        setFollowUpQuestions([]);
        setFollowupFromAnalysis(sanitized.followup_questions || []);
      } else if (data.status === 'follow_up') {
        setFollowUpQuestions(data.follow_up_questions || []);
        setError('');
      } else {
        setError(data.message || "Analysis failed after follow-up.");
      }
    } catch (err) {
      console.error('Follow-up submission error:', err);
      setError("Follow-up submission failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    if (!result?.patient_report) {
      setError('No report available to download.');
      return;
    }

    const blob = new Blob([result.patient_report], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'MediPath_AI_Report.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
            MediPath <span className="text-blue-600">AI</span> Dashboard
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-slate-500 mx-auto">
            Multi-Doctor AI Second Opinion + Cost-Optimized Diagnosis Engine
          </p>
          <p className="mt-2 text-sm text-red-600 font-medium">
            ⚠️ SAFETY NOTICE: This AI provides decision support only and is not a substitute for professional medical advice. Consult a qualified healthcare provider for diagnosis and treatment. In case of emergency, seek immediate medical attention.
          </p>
          {result && (
            <div className="mt-4 flex gap-3">
              <button
                type="button"
                onClick={() => setDoctorView(!doctorView)}
                className="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 transition-colors font-medium"
              >
                {doctorView ? '👁️ Patient View' : '👨‍⚕️ Doctor View'}
              </button>
              <button
                type="button"
                onClick={downloadReport}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                📥 Download Report
              </button>
            </div>
          )}
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column (Input & Doctors) */}
          <div className="lg:col-span-4 flex flex-col gap-6">
            <SymptomInput 
              symptoms={symptoms}
              setSymptoms={setSymptoms}
              patientData={patientData}
              setPatientData={setPatientData}
              onAnalyze={handleAnalyze}
              isLoading={loading}
              error={error}
              followUpQuestions={followUpQuestions}
              onFollowUpSubmit={handleFollowUpSubmit}
              followupFromAnalysis={followupFromAnalysis}
              onRefineDiagnosis={handleRefineDiagnosis}
            />
            
            {(loading || result) && (
               <DoctorSelection 
                 doctors={result?.doctor_opinions || []} 
                 isLoading={loading} 
               />
            )}
          </div>

          {/* Right Column (Results) */}
          <div className="lg:col-span-8 flex flex-col">
            {result && !loading ? (
              <div className="space-y-6 animate-fade-in flex flex-col h-full">
                {result && (
                  <DiagnosisCard 
                    diagnosis={String(result.diagnosis || 'Unknown').substring(0, 100)}
                    confidence={Number(result.confidence) || 0}
                    riskLevel={String(result.risk || 'Unknown')}
                    explanation={String(result.explanation || 'No explanation available').substring(0, 300)}
                  />
                )}

                <MultiHospitalSection hospitalOpinions={result.doctor_opinions} />
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-1">
                   <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                     <h3 className="text-lg font-bold text-slate-800 mb-4">💊 Optimized Tests</h3>
                     <TestRecommendations plan={result.tests} estimatedCost={result.estimated_cost || 0} />
                   </div>
                   <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                     <h3 className="text-lg font-bold text-slate-800 mb-4">📊 Analysis Metrics</h3>
                     <div className="space-y-3">
                       <div className="flex justify-between items-center p-2 bg-blue-50 rounded-lg">
                         <span className="text-sm font-medium text-slate-600">Confidence Score</span>
                         <span className="text-lg font-bold text-blue-600">{result.confidence}%</span>
                       </div>
                       <div className="flex justify-between items-center p-2 bg-red-50 rounded-lg">
                         <span className="text-sm font-medium text-slate-600">Risk Level</span>
                         <span className="text-lg font-bold text-red-600">{result.risk}</span>
                       </div>
                       <div className="flex justify-between items-center p-2 bg-green-50 rounded-lg">
                         <span className="text-sm font-medium text-slate-600">Total Tests</span>
                         <span className="text-lg font-bold text-green-600">{result.tests?.length || 0}</span>
                       </div>
                     </div>
                   </div>
                </div>

                {doctorView ? (
                  <>
                    <div className="bg-slate-50 rounded-2xl p-6 border border-slate-200">
                      <h3 className="text-lg font-bold text-slate-800 mb-4">AI Reasoning Details</h3>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-semibold text-slate-700">Confidence Breakdown</h4>
                          <p className="text-sm text-slate-600">Overall confidence: {result.confidence}%</p>
                          <p className="text-sm text-slate-600">Risk assessment: {result.risk}</p>
                        </div>
                        <div>
                          <h4 className="font-semibold text-slate-700">Doctor Consensus</h4>
                          <ul className="text-sm text-slate-600">
                            {result.doctor_opinions?.map((doc, idx) => (
                              <li key={idx}>• {doc.doctor}: {doc.diagnosis} ({doc.confidence})</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>

                    {/* Visualization Grid */}
                    {result.detailed_analysis && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <ConfidenceChart 
                          conditions={result.detailed_analysis.conditions}
                          confidences={result.detailed_analysis.confidence_scores}
                        />
                        <DoctorChart doctorOpinions={result.doctor_opinions} />
                        <RiskTimeline riskLevel={result.risk} />
                        <RiskMeter riskLevel={result.risk} />
                        <SymptomImpact symptoms={result.detailed_analysis.symptom_importance} />
                        <ClinicalInsights analysis={result.detailed_analysis} />
                      </div>
                    )}

                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                      <h3 className="text-lg font-bold text-slate-800 mb-4">Doctor Dashboard</h3>
                      <MultiHospitalSection hospitalOpinions={result.doctor_opinions} />
                      <TestRecommendations plan={result.tests} estimatedCost={result.estimated_cost || 0} />
                    </div>
                  </>
                ) : (
                  <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Clinical Report</h3>
                    <div className="bg-slate-50 p-4 rounded-lg max-h-96 overflow-y-auto">
                      <pre className="text-sm text-slate-700 whitespace-pre-wrap">{result.patient_report}</pre>
                    </div>
                    <button
                      type="button"
                      onClick={downloadReport}
                      className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      Download Report
                    </button>
                  </div>
                )}
              </div>
            ) : loading ? (
              <div className="h-full min-h-[400px] flex items-center justify-center p-12 bg-white rounded-2xl shadow-sm border border-slate-200">
                <div className="text-center">
                  <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-slate-500 font-medium animate-pulse text-lg">AI Specialists Analyzing...</p>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[400px] flex items-center justify-center p-12 bg-white/50 rounded-2xl border border-dashed border-slate-300">
                <p className="text-slate-400">Enter symptoms and patient information to begin analysis.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

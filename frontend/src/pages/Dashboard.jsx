import React, { useState } from 'react';
import SymptomInput from '../components/SymptomInput';
import DoctorSelection from '../components/DoctorSelection';
import DiagnosisCard from '../components/DiagnosisCard';
import AgreementChart from '../components/AgreementChart';
import TestRecommendations from '../components/TestRecommendations';
import { analyzeSymptoms } from '../services/api';

export default function Dashboard() {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!symptoms.trim()) {
      setError("Please enter symptoms");
      return;
    }
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await analyzeSymptoms(symptoms);
      setResult(data);
    } catch (err) {
      setError("Analysis failed. Please check if the backend is running.");
    } finally {
      setLoading(false);
    }
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
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column (Input & Doctors) */}
          <div className="lg:col-span-4 flex flex-col gap-6">
            <SymptomInput 
              symptoms={symptoms}
              setSymptoms={setSymptoms}
              onAnalyze={handleAnalyze}
              isLoading={loading}
              error={error}
            />
            
            {(loading || result) && (
               <DoctorSelection 
                 doctors={result?.selected_doctors || []} 
                 isLoading={loading} 
               />
            )}
          </div>

          {/* Right Column (Results) */}
          <div className="lg:col-span-8 flex flex-col">
            {result && !loading ? (
              <div className="space-y-6 animate-fade-in flex flex-col h-full">
                <DiagnosisCard 
                  diagnosis={result.final_diagnosis}
                  confidence={result.confidence}
                  riskLevel={result.risk_level}
                  explanation={result.explanation}
                />
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-1">
                   <AgreementChart contributions={result.doctor_contributions} />
                   <TestRecommendations plan={result.optimized_tests} estimatedCost={result.estimated_cost} />
                </div>
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
                <p className="text-slate-400">Enter symptoms and click Analyze to begin the simulation.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

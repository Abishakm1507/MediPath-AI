import { useState } from 'react';
import { analyzeSymptoms } from './services/api';
import SymptomInput from './components/SymptomInput';
import DoctorOpinions from './components/DoctorOpinions';
import CostOptimizerPanel from './components/CostOptimizerPanel';
import FinalDiagnosisPanel from './components/FinalDiagnosisPanel';

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!symptoms.trim()) {
      setError("Please enter some symptoms.");
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      const data = await analyzeSymptoms(symptoms);
      setResult(data);
    } catch (err) {
      setError("Failed to analyze symptoms. Ensure the backend is running.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
            MediPath <span className="text-blue-600">AI</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-slate-500 mx-auto">
            Multi-Doctor AI Second Opinion + Cost-Optimized Diagnosis Engine
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          
          {/* Left Column: Input and Final Diagnosis */}
          <div className="lg:col-span-1 space-y-8">
            <SymptomInput 
              symptoms={symptoms} 
              setSymptoms={setSymptoms} 
              onAnalyze={handleAnalyze} 
              isLoading={isLoading} 
              error={error} 
            />
            
            {result && result.final_diagnosis && (
              <FinalDiagnosisPanel 
                diagnosis={result.final_diagnosis} 
                confidence={result.confidence}
                reasoning={result.reasoning}
                aggregatedDiagnosis={result.aggregated_diagnosis}
              />
            )}
          </div>

          {/* Right Column: Doctor Opinions and Cost Optimization */}
          <div className="lg:col-span-2 space-y-8">
            {isLoading && (
              <div className="flex items-center justify-center p-12 bg-white rounded-2xl shadow-sm border border-slate-200">
                <div className="flex flex-col items-center space-y-4">
                  <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                  <p className="text-slate-500 font-medium animate-pulse">Consulting virtual specialists...</p>
                </div>
              </div>
            )}
            
            {!isLoading && result && (
              <div className="space-y-8 animate-fade-in">
                <DoctorOpinions opinions={result.doctor_opinions} />
                <CostOptimizerPanel plan={result.optimized_tests} />
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}

export default App;

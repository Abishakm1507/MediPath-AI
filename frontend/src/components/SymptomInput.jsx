import React from 'react';
import { Activity, AlertCircle } from 'lucide-react';

const SymptomInput = ({ symptoms, setSymptoms, onAnalyze, isLoading, error }) => {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-blue-50 rounded-lg">
            <Activity className="w-6 h-6 text-blue-600" />
          </div>
          <h2 className="text-xl font-bold text-slate-800">Patient Symptoms</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label htmlFor="symptoms" className="block text-sm font-medium text-slate-600 mb-2">
              Describe the symptoms in detail
            </label>
            <textarea
              id="symptoms"
              rows={6}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow resize-none"
              placeholder="E.g., Patient is a 45-year-old male with persistent dry cough, fever of 101F, and mild chest pain for the past 3 days..."
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg text-sm">
              <AlertCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}

          <button
            onClick={onAnalyze}
            disabled={isLoading}
            className={`w-full py-3 px-4 rounded-xl font-medium text-white transition-all transform active:scale-[0.98] ${
              isLoading 
                ? 'bg-slate-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'
            }`}
          >
            {isLoading ? 'Analyzing...' : 'Analyze Case'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SymptomInput;

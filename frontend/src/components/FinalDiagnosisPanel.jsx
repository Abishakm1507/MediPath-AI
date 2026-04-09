import React from 'react';
import { HeartPulse, CheckCircle2 } from 'lucide-react';

const FinalDiagnosisPanel = ({ diagnosis, confidence, reasoning, aggregatedDiagnosis }) => {
  if (!diagnosis) return null;

  // Convert confidence to a percentage string if it's a number, or just pass it if it's already a string
  const confValue = typeof confidence === 'number' 
    ? (confidence * 100).toFixed(0) + '%' 
    : confidence;

  return (
    <div className="bg-gradient-to-br from-blue-600 flex flex-col to-indigo-800 rounded-2xl shadow-lg border border-blue-500 overflow-hidden text-white animate-fade-in relative transition-transform transform">
      <div className="absolute top-0 right-0 p-8 opacity-10">
        <HeartPulse className="w-32 h-32" />
      </div>
      
      <div className="p-6 relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 backdrop-blur-sm rounded-lg">
              <CheckCircle2 className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-xl font-bold">Consensus Diagnosis</h2>
          </div>
          <div className="bg-white text-indigo-700 font-bold px-3 py-1 rounded-full text-sm shadow-sm flex items-center">
            {confValue} Confidence
          </div>
        </div>
        
        <div className="mb-6">
          <h3 className="text-3xl font-extrabold mb-2 tracking-tight">
            {diagnosis}
          </h3>
          <p className="text-blue-100 text-sm leading-relaxed">
            {reasoning}
          </p>
        </div>
      </div>
      
      {aggregatedDiagnosis && aggregatedDiagnosis.probability_distribution && (
        <div className="bg-white/10 backdrop-blur-md p-6 border-t border-white/20 mt-auto">
          <h4 className="text-xs uppercase tracking-wider text-blue-200 font-semibold mb-3">Differential Diagnosis Breakdown</h4>
          <div className="space-y-3">
            {Object.entries(aggregatedDiagnosis.probability_distribution).slice(0, 3).map(([disease, prob], idx) => (
              <div key={idx}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-white">{disease}</span>
                  <span className="text-blue-200">{(prob * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-black/20 rounded-full h-1.5">
                  <div 
                    className="bg-blue-300 h-1.5 rounded-full" 
                    style={{ width: `${Math.min(prob * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FinalDiagnosisPanel;

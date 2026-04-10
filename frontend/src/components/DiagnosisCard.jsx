import React from 'react';
import ConfidenceBar from './ConfidenceBar';
import RiskBadge from './RiskBadge';

export default function DiagnosisCard({ diagnosis, confidence, riskLevel, explanation }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-500 mb-1">Final Diagnosis</h2>
          <h1 className="text-3xl font-extrabold text-slate-900">{diagnosis}</h1>
        </div>
        <RiskBadge level={riskLevel} />
      </div>
      
      <p className="text-slate-600 italic mb-6">"{explanation}"</p>
      
      <ConfidenceBar confidence={confidence} />
    </div>
  );
}

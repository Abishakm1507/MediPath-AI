import React from 'react';
import ConfidenceBar from './ConfidenceBar';
import RiskBadge from './RiskBadge';

export default function DiagnosisCard({ diagnosis, confidence, riskLevel, explanation }) {
  // Defensive type checking and sanitization - handle objects gracefully
  const safeDiagnosis = typeof diagnosis === 'string' ? diagnosis : (diagnosis || 'Unknown Diagnosis');
  const safeConfidence = typeof confidence === 'number' ? confidence : 0;
  const safeRiskLevel = typeof riskLevel === 'string' ? riskLevel : 'Unknown';
  const safeExplanation = typeof explanation === 'string' ? explanation : (explanation?.key_factors || 'No explanation available');

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-500 mb-1">Final Diagnosis</h2>
          <h1 className="text-3xl font-extrabold text-slate-900">{safeDiagnosis}</h1>
        </div>
        <RiskBadge level={safeRiskLevel} />
      </div>
      
      <p className="text-slate-600 italic mb-6">"{safeExplanation}"</p>
      
      <ConfidenceBar confidence={safeConfidence} />
    </div>
  );
}

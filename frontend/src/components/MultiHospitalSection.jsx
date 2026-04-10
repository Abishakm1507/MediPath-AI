import React from 'react';
import { Building2 } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function MultiHospitalSection({ hospitalOpinions }) {
  // Ensure we have an array
  const opinions = Array.isArray(hospitalOpinions) ? hospitalOpinions : [];
  
  if (!opinions || opinions.length === 0) return null;

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mt-6">
      <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
        <Building2 className="text-blue-600" />
        Multi-Hospital Network Output
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {opinions.map((h, idx) => (
          <div key={idx} className="bg-slate-50 border border-slate-200 rounded-xl p-4 transition-all hover:shadow-md">
            <h4 className="font-bold text-lg text-slate-800 mb-1">{h.hospital_name}</h4>
            <div className="text-xs font-semibold text-blue-600 mb-3">{h.specialization}</div>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between items-center bg-white p-2 border border-slate-100 rounded-lg shadow-sm">
                <span className="text-slate-500 text-xs uppercase tracking-wider">Diagnosis</span>
                <span className="font-bold text-slate-800">{h.diagnosis}</span>
              </div>
              <div className="flex justify-between items-center bg-white p-2 border border-slate-100 rounded-lg shadow-sm">
                <span className="text-slate-500 text-xs uppercase tracking-wider">Confidence</span>
                <span className="font-bold text-emerald-600">{h.confidence}%</span>
              </div>
              <div className="flex justify-between items-center bg-white p-2 border border-slate-100 rounded-lg shadow-sm">
                <span className="text-slate-500 text-xs uppercase tracking-wider">Risk</span>
                <RiskBadge level={h.risk} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

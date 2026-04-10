import React from 'react';

export default function RiskBadge({ level }) {
  // Ensure level is a string - handle objects gracefully
  const riskLevel = typeof level === 'string' ? level : (typeof level === 'object' ? 'Unknown' : String(level || 'Unknown'));
  
  const riskStyles = {
    High: 'bg-red-100 text-red-700 border-red-200',
    Medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    Low: 'bg-green-100 text-green-700 border-green-200',
    Unknown: 'bg-slate-100 text-slate-700 border-slate-200'
  };

  const styleClass = riskStyles[riskLevel] || riskStyles['Unknown'];

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider ${styleClass}`}>
      {riskLevel} Risk
    </span>
  );
}

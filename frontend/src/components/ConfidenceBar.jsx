import React from 'react';

export default function ConfidenceBar({ confidence }) {
  const percentage = Math.min(100, Math.max(0, confidence || 0));
  
  return (
    <div className="mt-4">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-semibold text-slate-600">Confidence Score</span>
        <span className="text-sm font-bold text-slate-800">{percentage}%</span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
        <div 
          className="bg-blue-600 h-3 rounded-full transition-all duration-1000 ease-out" 
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}

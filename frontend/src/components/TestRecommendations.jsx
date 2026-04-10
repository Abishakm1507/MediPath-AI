import React from 'react';
import { analyzeSymptoms } from '../services/api';

const TestRecommendations = ({ plan, estimatedCost }) => {
  // Use CostOptimizerPanel functionality directly
  if (!plan || plan.length === 0) return null;

  const totalCost = estimatedCost !== undefined 
    ? estimatedCost 
    : (typeof plan[0] === 'object' ? plan.reduce((sum, item) => sum + (item.cost || 0), 0) : 0);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-emerald-100 overflow-hidden h-64 flex flex-col">
      <div className="bg-emerald-50/80 p-4 border-b border-emerald-100 flex justify-between items-center shrink-0">
        <h2 className="text-lg font-bold text-slate-800" style={{lineHeight: 1}}>Optimized Tests</h2>
        <div className="text-right">
          <div className="text-teal-700 font-bold text-xl">
            ₹{totalCost.toLocaleString()}
          </div>
        </div>
      </div>
      
      <div className="p-5 overflow-y-auto flex-1">
        <ul className="space-y-3">
          {plan.map((step, idx) => {
            const isObject = typeof step === 'object';
            const testName = isObject ? step.test : step;
            return (
              <li key={idx} className="flex items-center gap-3">
                <span className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-xs font-bold shrink-0">{idx + 1}</span>
                <span className="font-semibold text-slate-700 text-sm">{testName}</span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};
export default TestRecommendations;

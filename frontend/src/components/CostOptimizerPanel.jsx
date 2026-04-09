import React from 'react';
import { IndianRupee, ShieldCheck } from 'lucide-react';

const CostOptimizerPanel = ({ plan }) => {
  if (!plan || plan.length === 0) return null;

  const totalCost = plan.reduce((sum, item) => sum + item.cost, 0);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-emerald-100 overflow-hidden">
      <div className="bg-emerald-50/80 p-5 border-b border-emerald-100 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-100 rounded-lg text-emerald-700">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-slate-800">Optimized Diagnostic Plan</h2>
        </div>
        <div className="text-right">
          <p className="text-sm font-medium text-slate-500 uppercase tracking-wide">Expected Cost</p>
          <div className="flex items-center text-teal-700 font-bold text-2xl">
            <IndianRupee className="w-5 h-5 mr-1" />
            {totalCost.toLocaleString()}
          </div>
        </div>
      </div>
      
      <div className="p-5">
        <div className="space-y-4">
          {plan.map((step, idx) => (
            <div key={idx} className="flex relative">
              {idx !== plan.length - 1 && (
                <div className="absolute top-8 bottom-[-16px] left-5 w-0.5 bg-emerald-100 z-0"></div>
              )}
              <div className="relative z-10 flex-shrink-0 w-10 h-10 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold mr-4 shadow-sm">
                {step.step}
              </div>
              <div className="flex-1 bg-slate-50 border border-slate-100 rounded-xl p-4 transition-all hover:bg-slate-100">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-slate-800 text-lg">{step.test}</h3>
                  <div className="flex items-center text-emerald-700 font-medium">
                    <IndianRupee className="w-4 h-4 mr-0.5" />
                    {step.cost.toLocaleString()}
                  </div>
                </div>
                <p className="text-sm text-slate-600">{step.reason}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CostOptimizerPanel;

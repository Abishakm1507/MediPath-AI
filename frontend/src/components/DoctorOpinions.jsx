import React from 'react';
import { Stethoscope, UserCog } from 'lucide-react';

const DoctorOpinionCard = ({ title, opinion }) => {
  const { diseases = [], confidence = [], tests = [], reasoning = "No reasoning provided." } = opinion || {};
  
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow">
      <div className="border-b border-slate-100 bg-slate-50/50 p-4 flex items-center space-x-3">
        <div className="p-2 bg-indigo-100 rounded-lg">
          {title.includes("Physician") ? (
            <UserCog className="w-5 h-5 text-indigo-600" />
          ) : (
            <Stethoscope className="w-5 h-5 text-indigo-600" />
          )}
        </div>
        <h3 className="font-semibold text-slate-800">{title}</h3>
      </div>
      
      <div className="p-5 space-y-4">
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Predictions</h4>
          <div className="space-y-2">
            {diseases.length > 0 ? diseases.map((disease, idx) => (
              <div key={idx} className="flex justify-between items-center text-sm">
                <span className="text-slate-700 font-medium">{disease}</span>
                <span className="bg-indigo-50 text-indigo-700 py-1 px-2 rounded-md font-semibold">
                  {((confidence[idx] || 0) * 100).toFixed(1)}%
                </span>
              </div>
            )) : <p className="text-sm text-slate-500">No predictions available</p>}
          </div>
        </div>
        
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Recommended Tests</h4>
          <div className="flex flex-wrap gap-2">
            {tests.length > 0 ? tests.map((test, idx) => (
              <span key={idx} className="bg-slate-100 text-slate-600 text-xs py-1 px-2 rounded-md">
                {test}
              </span>
            )) : <span className="text-xs text-slate-500">None</span>}
          </div>
        </div>
        
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Reasoning</h4>
          <p className="text-sm text-slate-600 italic">"{reasoning}"</p>
        </div>
      </div>
    </div>
  );
};

const DoctorOpinions = ({ opinions }) => {
  if (!opinions) return null;
  
  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-4 flex items-center">
        <span className="bg-indigo-600 w-2 h-6 rounded-full mr-3 block"></span>
        Specialist Breakdown
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(opinions).map(([doctorName, opinionData]) => (
          <DoctorOpinionCard 
            key={doctorName} 
            title={doctorName} 
            opinion={opinionData} 
          />
        ))}
      </div>
    </div>
  );
};

export default DoctorOpinions;

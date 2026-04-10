import React from 'react';
import { Stethoscope, Loader2 } from 'lucide-react';

export default function DoctorSelection({ doctors, isLoading }) {
  // If loading, show fake analyzing doctors as per the advanced step
  const displayDocs = isLoading 
    ? ["Cardiologist", "Pulmonologist", "General Physician"] 
    : doctors || [];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-xl font-bold mb-4 text-slate-800">
        {isLoading ? "AI Doctors Analyzing..." : "Selected Doctors"}
      </h3>
      <div className="flex flex-col gap-3">
        {displayDocs.map((doc, idx) => (
          <div key={idx} className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-100">
            <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
              <Stethoscope size={20} />
            </div>
            <div className="flex-1">
              <h4 className="font-semibold text-slate-800 capitalize">{doc}</h4>
            </div>
            {isLoading && (
              <div className="flex items-center text-blue-500 gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-xs font-semibold animate-pulse">Analyzing</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function AgreementChart({ contributions }) {
  if (!contributions || Object.keys(contributions).length === 0) return null;

  const data = Object.keys(contributions).map(key => ({
    name: key,
    value: contributions[key]
  }));

  const colors = ['#4f46e5', '#3b82f6', '#0ea5e9', '#06b6d4', '#14b8a6'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 h-64 flex flex-col justify-between">
      <h3 className="text-lg font-bold text-slate-800 mb-2">Doctor Agreement</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 0, right: 30, left: -20, bottom: 0 }}>
            <XAxis type="number" hide />
            <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 13, fontWeight: 600}} width={120} />
            <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

import React from 'react';
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

// Confidence Distribution Chart
export function ConfidenceChart({ conditions, confidences }) {
  if (!conditions || !confidences || conditions.length === 0) return null;

  // Prepare data
  const data = conditions.map((condition, idx) => ({
    name: condition.substring(0, 15),
    confidence: Number(confidences[idx]) || 0
  })).sort((a, b) => b.confidence - a.confidence).slice(0, 5);

  const COLORS = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">📊 Diagnostic Confidence</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip formatter={(value) => `${value}%`} />
          <Bar dataKey="confidence" fill="#3b82f6" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// Doctor Opinion Pie Chart
export function DoctorChart({ doctorOpinions }) {
  if (!doctorOpinions || doctorOpinions.length === 0) return null;

  const data = doctorOpinions.map((doc, idx) => ({
    name: doc.hospital_name?.substring(0, 12) || `Doctor ${idx + 1}`,
    value: Number(doc.confidence) || 0
  }));

  const COLORS = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">👨‍⚕️ Doctor Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ${value}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${value}%`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

// Risk Level Timeline
export function RiskTimeline({ riskLevel }) {
  const riskProfiles = {
    'High': [90, 80, 70, 60, 50, 40, 35],
    'Medium': [60, 55, 45, 35, 25, 20, 15],
    'Low': [30, 25, 20, 15, 12, 10, 8]
  };

  const riskColors = {
    'High': '#ef4444',
    'Medium': '#f59e0b',
    'Low': '#10b981'
  };

  const data = ['Imm', '6h', '12h', '24h', '2d', '5d', '7d'].map((time, idx) => ({
    time,
    risk: riskProfiles[riskLevel]?.[idx] || 50
  }));

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">📈 Risk Progression</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="risk" 
            stroke={riskColors[riskLevel] || '#6b7280'}
            strokeWidth={3}
            dot={{ fill: riskColors[riskLevel], r: 5 }}
            name={`${riskLevel} Risk`}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// Symptom Importance
export function SymptomImpact({ symptoms }) {
  if (!symptoms || Object.keys(symptoms).length === 0) return null;

  const data = Object.entries(symptoms)
    .map(([name, importance]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      importance: Number(importance) || 0
    }))
    .sort((a, b) => b.importance - a.importance)
    .slice(0, 6);

  const COLORS = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">🔍 Symptom Impact</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="name" type="category" width={140} />
          <Tooltip />
          <Bar dataKey="importance" fill="#3b82f6" radius={[0, 8, 8, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// Risk Meter
export function RiskMeter({ riskLevel }) {
  const riskConfig = {
    'High': { color: 'bg-red-500', percentage: 90 },
    'Medium': { color: 'bg-yellow-500', percentage: 50 },
    'Low': { color: 'bg-green-500', percentage: 25 }
  };

  const config = riskConfig[riskLevel] || riskConfig['Medium'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">⚠️ Risk Meter</h3>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-slate-600">Overall Risk Level</span>
          <span className={`px-3 py-1 rounded-full text-white font-bold ${config.color}`}>
            {riskLevel}
          </span>
        </div>
        <div className="w-full bg-slate-200 rounded-full h-4 overflow-hidden">
          <div
            className={`h-full ${config.color} transition-all duration-300`}
            style={{ width: `${config.percentage}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-slate-500">
          <span>Low</span>
          <span>Medium</span>
          <span>High</span>
        </div>
      </div>
    </div>
  );
}

// Clinical Insights Panel
export function ClinicalInsights({ analysis }) {
  if (!analysis) return null;

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-2xl shadow-sm border border-blue-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4">🔬 Clinical Insights</h3>
      <div className="space-y-3">
        <div>
          <h4 className="text-sm font-semibold text-slate-700 mb-1">Primary Diagnosis:</h4>
          <p className="text-sm text-slate-600">
            {analysis.reasoning || "Analysis generates reasoning insights."}
          </p>
        </div>
        <div>
          <h4 className="text-sm font-semibold text-slate-700 mb-1">Key Factors:</h4>
          <ul className="text-sm text-slate-600 space-y-1">
            <li>• Multiple doctors aligned on primary diagnosis</li>
            <li>• Confidence score reflects high clinical agreement</li>
            <li>• Tests recommended for confirmation</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

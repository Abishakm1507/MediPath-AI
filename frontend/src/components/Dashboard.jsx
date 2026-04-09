import { useState } from "react";

export default function Dashboard() {
  const [symptoms, setSymptoms] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!symptoms.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms }),
      });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="w-full max-w-5xl bg-white shadow-xl rounded-2xl overflow-hidden flex flex-col md:flex-row min-h-[600px] border border-gray-100">
      {/* Sidebar: Inputs */}
      <div className="w-full md:w-1/3 p-6 md:p-8 bg-gray-50 flex flex-col border-r border-gray-100">
        <h2 className="text-lg font-bold text-gray-800 mb-4">Check Symptoms</h2>
        <p className="text-sm text-gray-500 mb-4">Describe the patient's symptoms below for a multi-specialist AI analysis.</p>
        <textarea
          className="w-full p-4 text-sm border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none transition-shadow bg-white shadow-sm"
          rows="6"
          placeholder="e.g. Patient has a high fever, severe cough, and chest pain for 3 days..."
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
        ></textarea>
        <button
          onClick={handleAnalyze}
          disabled={loading || !symptoms.trim()}
          className="mt-6 w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold rounded-xl transition-all shadow-md active:scale-[0.98] disabled:opacity-50 flex justify-center items-center"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Analyzing...
            </span>
          ) : "Analyze Now"}
        </button>
        {error && <p className="text-red-500 mt-4 text-sm">{error}</p>}
      </div>

      {/* Main Content: Results */}
      <div className="w-full md:w-2/3 p-6 md:p-8 bg-white overflow-y-auto">
        {!result && !loading && (
          <div className="h-full flex flex-col items-center justify-center text-gray-400">
            <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <p className="font-medium">Waiting for symptoms input.</p>
          </div>
        )}

        {loading && (
          <div className="h-full flex flex-col items-center justify-center text-blue-500">
            <div className="flex gap-2 mb-4">
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
            <p className="font-semibold text-gray-600 animate-pulse">Running Multiple AI Doctors in Parallel...</p>
          </div>
        )}

        {result && !loading && (
          <div className="space-y-8 animate-fade-in">
            {/* Final Diagnosis Card */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 p-6 rounded-2xl shadow-sm">
              <h3 className="text-sm font-bold text-blue-800 uppercase tracking-wider mb-2">Final Conclusion</h3>
              <div className="flex justify-between items-end mb-4">
                <h2 className="text-3xl font-extrabold text-gray-900">{result.final_diagnosis}</h2>
                <span className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-bold shadow-sm">Confidence: {result.confidence}</span>
              </div>
              <p className="text-gray-700 leading-relaxed mb-4">{result.reasoning}</p>
              
              <div className="mt-4">
                <h4 className="text-sm font-semibold text-gray-800 mb-2">Recommended Next Steps:</h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                  {result.recommended_next_steps?.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Diagnostic Cost Optimizer */}
            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                Optimal Test Plan
              </h3>
              <div className="bg-white border text-sm text-gray-700 border-gray-200 rounded-xl overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Step</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Test</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Cost</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Reason</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 bg-white">
                    {result.cost_optimized_plan?.map((item, idx) => (
                      <tr key={idx} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 font-semibold text-gray-900">{item.step}</td>
                        <td className="px-4 py-3 font-medium text-indigo-600">{item.test}</td>
                        <td className="px-4 py-3">₹{item.cost}</td>
                        <td className="px-4 py-3 text-xs text-gray-500">{item.reason}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Doctors Opinions */}
            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                AI Specialist Opinions
              </h3>
              <div className="grid grid-cols-1 gap-4">
                {Object.entries(result.doctor_opinions || {}).map(([name, opinion]) => (
                  <div key={name} className="border border-gray-100 p-4 rounded-xl shadow-sm bg-white hover:shadow-md transition-shadow flex flex-col gap-2">
                    <div className="flex justify-between items-center bg-gray-50 -mx-4 -mt-4 p-4 rounded-t-xl mb-2 border-b border-gray-100">
                      <h4 className="font-bold text-gray-800">{name}</h4>
                    </div>
                    <div className="text-sm">
                      <p className="font-semibold text-gray-600 mb-1">Top Predictions:</p>
                      <div className="flex flex-wrap gap-2 mb-3">
                        {Object.entries(opinion?.disease_predictions || {}).map(([disease, prob]) => (
                          <span key={disease} className="bg-indigo-50 text-indigo-700 px-2 py-1 rounded text-xs border border-indigo-100">
                            {disease}: {(prob * 100).toFixed(0)}%
                          </span>
                        ))}
                      </div>
                      <p className="text-gray-700 italic border-l-2 border-indigo-200 pl-3">"{opinion?.reasoning || 'No reasoning provided.'}"</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}

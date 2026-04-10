import React, { useState } from 'react';
import { Activity, AlertCircle, AlertTriangle } from 'lucide-react';

const SymptomInput = ({
  symptoms, setSymptoms,
  patientData, setPatientData,
  onAnalyze, isLoading, error,
  followUpQuestions, onFollowUpSubmit,
  followupFromAnalysis, onRefineDiagnosis
}) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [followUpResponses, setFollowUpResponses] = useState({});

  const handlePatientDataChange = (field, value) => {
    setPatientData(prev => ({ ...prev, [field]: value }));
  };

  const handleFollowUpChange = (question, value) => {
    setFollowUpResponses(prev => ({ ...prev, [question]: value }));
  };

  const handleNextStep = () => {
    if (currentStep === 1 && symptoms.trim()) {
      setCurrentStep(2);
    }
  };

  const handleSubmitFollowUpFromAnalysis = () => {
    if (onRefineDiagnosis) {
      onRefineDiagnosis(followUpResponses);
    }
  };

  const handleSubmitFollowUp = () => {
    if (onFollowUpSubmit) {
      onFollowUpSubmit(followUpResponses);
    }
  };

  const renderFollowUp = () => (
    <>
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-yellow-50 rounded-lg">
          <AlertTriangle className="w-6 h-6 text-yellow-600" />
        </div>
        <h2 className="text-xl font-bold text-slate-800">Additional Information Needed</h2>
      </div>

      <div className="space-y-4">
        {followUpQuestions.map((question, index) => (
          <div key={index}>
            <label className="block text-sm font-medium text-slate-600 mb-2">
              {question}
            </label>
            <input
              type="text"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={followUpResponses[question] || ''}
              onChange={(e) => handleFollowUpChange(question, e.target.value)}
            />
          </div>
        ))}

        <button
          onClick={handleSubmitFollowUp}
          disabled={isLoading}
          className={`w-full py-3 px-4 rounded-xl font-medium text-white transition-all transform active:scale-[0.98] ${
            isLoading
              ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'
          }`}
        >
          {isLoading ? 'Submitting...' : 'Submit & Analyze'}
        </button>
      </div>
    </>
  );

  const renderStep1 = () => (
    <>
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-blue-50 rounded-lg">
          <Activity className="w-6 h-6 text-blue-600" />
        </div>
        <h2 className="text-xl font-bold text-slate-800">Step 1: Patient Symptoms</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="symptoms" className="block text-sm font-medium text-slate-600 mb-2">
            Describe the symptoms in detail
          </label>
          <textarea
            id="symptoms"
            rows={6}
            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow resize-none"
            placeholder="E.g., Patient has persistent dry cough, fever of 101F, and mild chest pain..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            disabled={isLoading}
          />
        </div>

        <button
          type="button"
          onClick={handleNextStep}
          disabled={isLoading || !symptoms.trim()}
          className={`w-full py-3 px-4 rounded-xl font-medium text-white transition-all transform active:scale-[0.98] ${
            isLoading || !symptoms.trim()
              ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'
          }`}
        >
          Next: Patient Information
        </button>
      </div>
    </>
  );

  const renderStep2 = () => (
    <>
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-blue-50 rounded-lg">
          <Activity className="w-6 h-6 text-blue-600" />
        </div>
        <h2 className="text-xl font-bold text-slate-800">Step 2: Patient Information</h2>
      </div>

      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-2">Age</label>
            <input
              type="number"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., 45"
              value={patientData.age || ''}
              onChange={(e) => handlePatientDataChange('age', e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-2">Gender</label>
            <select
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={patientData.gender || ''}
              onChange={(e) => handlePatientDataChange('gender', e.target.value)}
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-2">Duration</label>
            <input
              type="text"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., 3 days"
              value={patientData.duration || ''}
              onChange={(e) => handlePatientDataChange('duration', e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-2">Severity</label>
            <select
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={patientData.severity || ''}
              onChange={(e) => handlePatientDataChange('severity', e.target.value)}
            >
              <option value="">Select severity</option>
              <option value="mild">Mild</option>
              <option value="moderate">Moderate</option>
              <option value="severe">Severe</option>
            </select>
          </div>
        </div>

        <div className="flex space-x-3">
          <button
            type="button"
            onClick={() => setCurrentStep(1)}
            className="flex-1 py-3 px-4 rounded-xl font-medium text-slate-600 border border-slate-200 hover:bg-slate-50 transition-all"
          >
            Back
          </button>
          <button
            type="button"
            onClick={onAnalyze}
            disabled={isLoading}
            className={`flex-1 py-3 px-4 rounded-xl font-medium text-white transition-all transform active:scale-[0.98] ${
              isLoading
                ? 'bg-slate-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'
            }`}
          >
            {isLoading ? 'Analyzing...' : 'Analyze Case'}
          </button>
        </div>
      </div>
    </>
  );

  const renderFollowUpFromAnalysis = () => {
    // Filter and ensure questions are strings
    const validQuestions = (followupFromAnalysis || []).filter(q => typeof q === 'string');
    
    if (!validQuestions.length) {
      return <div className="text-slate-600 p-4 bg-slate-50 rounded-lg">No additional questions available.</div>;
    }

    return (
      <>
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-blue-50 rounded-lg">
            <Activity className="w-6 h-6 text-blue-600" />
          </div>
          <h2 className="text-xl font-bold text-slate-800">Follow-Up Questions</h2>
        </div>

        <div className="space-y-4">
          <p className="text-slate-600">To refine your diagnosis, please answer these additional questions:</p>
          
          {validQuestions.map((question, index) => (
            <div key={index}>
              <label className="block text-sm font-medium text-slate-600 mb-2">
                {String(question).substring(0, 200)}
              </label>
              <textarea
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={2}
                value={followUpResponses[question] || ''}
                onChange={(e) => handleFollowUpChange(question, e.target.value)}
                placeholder="Your answer..."
              />
            </div>
          ))}

          <button
            type="button"
            onClick={handleSubmitFollowUpFromAnalysis}
            disabled={isLoading}
            className={`w-full py-3 px-4 rounded-xl font-medium text-white transition-all transform active:scale-[0.98] ${
              isLoading
                ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700 hover:shadow-md'
          }`}
        >
          {isLoading ? 'Refining Diagnosis...' : 'Submit & Refine Diagnosis'}
        </button>
      </div>
      </>
    );
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="p-6">
        {(followupFromAnalysis && followupFromAnalysis.length > 0 && followupFromAnalysis.some(q => typeof q === 'string')) ? renderFollowUpFromAnalysis() :
         (followUpQuestions && followUpQuestions.length > 0) ? renderFollowUp() :
         currentStep === 1 ? renderStep1() : renderStep2()}

        {error && (
          <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg text-sm mt-4">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default SymptomInput;

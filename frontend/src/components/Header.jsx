export default function Header() {
  return (
    <header className="w-full max-w-5xl py-6 flex justify-between items-center mb-4">
      <div>
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
          MediPath AI
        </h1>
        <p className="text-gray-600 mt-2 font-medium">Multi-Doctor AI Second Opinion + Cost-Optimized Diagnosis Engine</p>
      </div>
      <div className="hidden sm:block">
        <span className="bg-indigo-100 text-indigo-800 text-sm font-semibold mr-2 px-3 py-1 rounded-full border border-indigo-200">
          v1.0.0
        </span>
      </div>
    </header>
  )
}

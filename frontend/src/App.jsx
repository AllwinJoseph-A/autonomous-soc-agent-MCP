import { useState } from 'react'

function App() {
  const [alertText, setAlertText] = useState('')
  const [report, setReport] = useState(null)
  const [evidence, setEvidence] = useState([]) // <-- NEW: State for our audit trail
  const [loading, setLoading] = useState(false)

  const handleInvestigate = async () => {
    if (!alertText) return
    setLoading(true)
    setReport(null)
    setEvidence([])

    try {
      const response = await fetch('http://127.0.0.1:8000/investigate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: alertText })
      })
      
      const data = await response.json()
      setReport(data.investigation_report)
      setEvidence(data.evidence || []) // <-- NEW: Save the evidence
    } catch (error) {
      setReport("Error connecting to the backend. Is FastAPI running on port 8000?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto font-sans">
      
      <header className="mb-8 border-b border-slate-700 pb-4">
        <h1 className="text-3xl font-bold text-cyan-400">Autonomous SOC Platform</h1>
        <p className="text-slate-400 text-sm mt-1">Powered by Local LLM & MCP Microservices</p>
      </header>

      <main className="space-y-6">
        
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-xl">
          <label className="block text-sm font-medium text-slate-300 mb-2">Incoming SIEM Alert</label>
          <textarea
            className="w-full bg-slate-900 border border-slate-600 rounded p-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 font-mono text-sm"
            rows="3"
            placeholder="e.g., Rahul logged in from IP address 103.45.67.89"
            value={alertText}
            onChange={(e) => setAlertText(e.target.value)}
          />
          <button
            onClick={handleInvestigate}
            disabled={loading || !alertText}
            className="mt-4 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-2 px-6 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Agent is hunting (Check Terminal)...' : 'Trigger Investigation'}
          </button>
        </div>

        {/* --- NEW: Agent Audit Trail Section --- */}
        {evidence.length > 0 && (
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-xl animate-fade-in">
            <h2 className="text-lg font-semibold text-amber-400 mb-4 flex items-center">
              <span className="mr-2">⚡</span> Agent Execution Trail
            </h2>
            <div className="space-y-3">
              {evidence.map((item, index) => (
                <div key={index} className="bg-slate-900 border border-slate-700 p-3 rounded flex flex-col">
                  <span className="text-xs font-bold text-cyan-500 uppercase tracking-wider mb-1">
                    Executed: {item.server} -> {item.tool}
                  </span>
                  <span className="text-sm text-slate-300 font-mono">{item.details}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Final Report Section */}
        {report && (
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-xl animate-fade-in">
            <h2 className="text-lg font-semibold text-emerald-400 mb-4 flex items-center">
              <span className="mr-2">✓</span> Final Investigation Report
            </h2>
            <div className="bg-slate-900 p-4 rounded border border-slate-700">
              <pre className="whitespace-pre-wrap text-slate-300 font-mono text-sm leading-relaxed">
                {report}
              </pre>
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App
import React, { useState } from 'react'

function ResultsDisplay({ result }) {
  const [expandedIndex, setExpandedIndex] = useState(null)
  
  if (!result) return null

  // Handle run_all results differently
  if (result.runAll) {
    const { summary, results } = result
    
    return (
      <div className="card">
        <div className="result-header">
          <h2>📋 Run All Results</h2>
          <div className={`status ${result.success ? 'status-success' : 'status-error'}`}>
            <span>{result.success ? '✓' : '✗'}</span>
            <span>{summary.successful}/{summary.total_operations} Passed</span>
          </div>
        </div>

        <div className="mb-2">
          <p className="text-secondary">
            <strong>Total Time:</strong> <code>{summary.total_time_ms.toFixed(0)}ms</code>
          </p>
          <p className="text-secondary">
            <strong>Success Rate:</strong> <code>{((summary.successful / summary.total_operations) * 100).toFixed(1)}%</code>
          </p>
        </div>

        <h3>Individual Results ({results.length} operations):</h3>
        <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
          {results.map((res, index) => (
            <div 
              key={index} 
              style={{ 
                marginBottom: '0.5rem',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                borderRadius: '6px',
                border: `1px solid ${res.success ? 'var(--accent-success)' : 'var(--accent-error)'}`
              }}
            >
              <div 
                style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  cursor: 'pointer'
                }}
                onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span>{res.success ? '✅' : '❌'}</span>
                  <code>{res.operation}()</code>
                  <span className="text-muted" style={{ fontSize: '0.875rem' }}>
                    {res.execution_time_ms}ms
                  </span>
                </div>
                <span style={{ fontSize: '0.875rem' }}>
                  {expandedIndex === index ? '▼' : '▶'}
                </span>
              </div>
              
              {expandedIndex === index && (
                <div className="code-block" style={{ marginTop: '0.5rem', fontSize: '0.75rem' }}>
                  <pre>{JSON.stringify(res.success ? res.result : { error: res.error }, null, 2)}</pre>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-2">
          <p className="text-muted">
            💡 <strong>Tip:</strong> Check the Jaeger UI to see all {results.length} distributed traces.
          </p>
        </div>
      </div>
    )
  }

  // Original single operation display
  return (
    <div className="card">
      <div className="result-header">
        <h2>📋 Execution Results</h2>
        <div className={`status ${result.success ? 'status-success' : 'status-error'}`}>
          <span>{result.success ? '✓' : '✗'}</span>
          <span>{result.success ? 'Success' : 'Failed'}</span>
        </div>
      </div>

      <div className="mb-2">
        <p className="text-secondary">
          <strong>Operation:</strong> <code>{result.operation}()</code>
        </p>
        {result.executionTime && (
          <p className="text-secondary">
            <strong>Execution Time:</strong> <code>{result.executionTime}ms</code>
          </p>
        )}
      </div>

      {result.success ? (
        <div>
          <h3>Response Data:</h3>
          <div className="code-block">
            <pre>{JSON.stringify(result.data, null, 2)}</pre>
          </div>
        </div>
      ) : (
        <div>
          <h3 style={{ color: 'var(--accent-error)' }}>Error:</h3>
          <div className="code-block" style={{ borderColor: 'var(--accent-error)' }}>
            <pre>{result.error}</pre>
          </div>
        </div>
      )}

      <div className="mt-2">
        <p className="text-muted">
          💡 <strong>Tip:</strong> Check the Jaeger UI to see the distributed trace for this operation.
        </p>
      </div>
    </div>
  )
}

export default ResultsDisplay

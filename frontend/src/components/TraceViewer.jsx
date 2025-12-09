import React from 'react'

function TraceViewer() {
    const jaegerUrl = 'http://localhost:16686'

    return (
        <div className="card">
            <div className="flex-between mb-2">
                <h2>📊 Observability Traces</h2>
                <a
                    href={jaegerUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary"
                >
                    <span>🔗</span>
                    <span>Open Jaeger UI</span>
                </a>
            </div>

            <p className="text-muted">
                View distributed traces for all MongoDB operations in Jaeger.
                Each operation executed from this dashboard will create trace spans
                that you can inspect in the Jaeger UI.
            </p>

            <div className="mt-2">
                <p className="text-secondary">
                    <strong>Service Name:</strong> <code>pymongo-testing</code>
                </p>
                <p className="text-secondary mt-1">
                    <strong>Jaeger UI:</strong> <a href={jaegerUrl} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-primary)' }}>{jaegerUrl}</a>
                </p>
            </div>
        </div>
    )
}

export default TraceViewer

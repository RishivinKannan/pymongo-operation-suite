import React, { useState, useEffect } from 'react'
import { io } from 'socket.io-client'

function ProgressModal({ onClose }) {
    const [progress, setProgress] = useState({
        type: 'idle',
        current: 0,
        total: 0,
        message: 'Initializing...',
        operations: []
    })
    const [isComplete, setIsComplete] = useState(false)

    useEffect(() => {
        // Connect to WebSocket
        const socket = io('http://localhost:5000')

        socket.on('connect', () => {
            console.log('WebSocket connected')
        })

        socket.on('progress', (data) => {
            console.log('Progress update:', data)

            if (data.type === 'start') {
                setProgress(prev => ({
                    ...prev,
                    type: 'running',
                    total: data.total,
                    message: data.message,
                    operations: []
                }))
            } else if (data.type === 'operation_start') {
                setProgress(prev => ({
                    ...prev,
                    current: data.current,
                    message: data.message
                }))
            } else if (data.type === 'operation_complete') {
                setProgress(prev => ({
                    ...prev,
                    current: data.current,
                    message: data.message,
                    operations: [...prev.operations, {
                        name: data.operation,
                        success: data.success,
                        time: data.execution_time_ms,
                        error: data.error
                    }]
                }))
            } else if (data.type === 'complete') {
                setProgress(prev => ({
                    ...prev,
                    type: 'complete',
                    message: data.message,
                    summary: data.summary
                }))
                setIsComplete(true)
            }
        })

        return () => {
            socket.disconnect()
        }
    }, [])

    const progressPercent = progress.total > 0
        ? (progress.current / progress.total) * 100
        : 0

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '700px' }}>
                <div className="modal-header">
                    <h2>⚡ Running All Operations</h2>
                    {isComplete && (
                        <button className="btn btn-sm" onClick={onClose}>
                            Close
                        </button>
                    )}
                </div>

                <div className="modal-body">
                    {/* Progress Bar */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            marginBottom: '0.5rem',
                            fontSize: '0.875rem'
                        }}>
                            <span>{progress.message}</span>
                            <span>{progress.current}/{progress.total}</span>
                        </div>
                        <div style={{
                            height: '8px',
                            background: 'var(--bg-tertiary)',
                            borderRadius: '4px',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                height: '100%',
                                width: `${progressPercent}%`,
                                background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))',
                                transition: 'width 0.3s ease'
                            }} />
                        </div>
                    </div>

                    {/* Summary (when complete) */}
                    {progress.summary && (
                        <div className="card" style={{
                            marginBottom: '1rem',
                            background: 'var(--bg-tertiary)',
                            border: `1px solid ${progress.summary.failed === 0 ? 'var(--accent-success)' : 'var(--accent-warning)'}`
                        }}>
                            <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent-success)' }}>
                                        {progress.summary.successful}
                                    </div>
                                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Passed</div>
                                </div>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent-error)' }}>
                                        {progress.summary.failed}
                                    </div>
                                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Failed</div>
                                </div>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent-primary)' }}>
                                        {Math.round(progress.summary.total_time_ms)}ms
                                    </div>
                                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Total Time</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Operations List */}
                    <div style={{
                        maxHeight: '400px',
                        overflowY: 'auto',
                        background: 'var(--bg-tertiary)',
                        borderRadius: '6px',
                        padding: '0.5rem'
                    }}>
                        {progress.operations.map((op, index) => (
                            <div
                                key={index}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'space-between',
                                    padding: '0.5rem',
                                    marginBottom: '0.25rem',
                                    background: 'var(--bg-secondary)',
                                    borderRadius: '4px',
                                    border: `1px solid ${op.success ? 'var(--accent-success)' : 'var(--accent-error)'}`,
                                    fontSize: '0.875rem'
                                }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <span>{op.success ? '✅' : '❌'}</span>
                                    <code>{op.name}()</code>
                                    {op.error && (
                                        <span style={{ color: 'var(--accent-error)', fontSize: '0.75rem' }}>
                                            {op.error.substring(0, 40)}...
                                        </span>
                                    )}
                                </div>
                                <span className="text-muted">{Math.round(op.time)}ms</span>
                            </div>
                        ))}

                        {/* Current operation indicator */}
                        {!isComplete && progress.current > 0 && (
                            <div style={{
                                padding: '0.75rem',
                                textAlign: 'center',
                                color: 'var(--accent-primary)',
                                animation: 'pulse 1.5s ease-in-out infinite'
                            }}>
                                ⏳ Processing...
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
        </div>
    )
}

export default ProgressModal

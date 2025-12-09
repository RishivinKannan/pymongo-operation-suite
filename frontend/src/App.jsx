import React, { useState, useEffect } from 'react'
import axios from 'axios'
import TestDashboard from './components/TestDashboard'
import TraceViewer from './components/TraceViewer'
import { SnackbarProvider } from './components/Snackbar'

const API_BASE = 'http://localhost:5000'

function App() {
    const [health, setHealth] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        checkHealth()
    }, [])

    const checkHealth = async () => {
        try {
            const response = await axios.get(`${API_BASE}/health`)
            setHealth(response.data)
        } catch (error) {
            console.error('Health check failed:', error)
            setHealth({ status: 'unhealthy', error: error.message })
        } finally {
            setLoading(false)
        }
    }

    return (
        <SnackbarProvider>
            <div className="app">
                <div className="header">
                    <div className="container">
                        <h1>🔍 PyMongo Testing Dashboard</h1>
                        <p className="subtitle">
                            Test all 35 MongoDB Collection methods with real-time observability
                        </p>

                        {!loading && (
                            <div className="flex-center gap-2 mt-2">
                                <div className={`status ${health?.status === 'healthy' ? 'status-success' : 'status-error'}`}>
                                    <span>{health?.status === 'healthy' ? '✓' : '✗'}</span>
                                    <span>API: {health?.status || 'Unknown'}</span>
                                </div>

                                {health?.observability && (
                                    <>
                                        <div className="status status-success">
                                            <span>✓</span>
                                            <span>OpenTelemetry</span>
                                        </div>
                                        {health.observability.datadog && (
                                            <div className="status status-success">
                                                <span>✓</span>
                                                <span>Datadog</span>
                                            </div>
                                        )}
                                        {health.observability.atatus && (
                                            <div className="status status-success">
                                                <span>✓</span>
                                                <span>Atatus</span>
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                <div className="container">
                    <TraceViewer />
                    <TestDashboard apiBase={API_BASE} />
                </div>
            </div>
        </SnackbarProvider>
    )
}

export default App

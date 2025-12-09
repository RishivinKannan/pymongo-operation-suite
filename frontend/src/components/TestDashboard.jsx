import React, { useState } from 'react'
import axios from 'axios'
import TestRunner from './TestRunner'
import ResultsDisplay from './ResultsDisplay'
import ProgressModal from './ProgressModal'
import ConfirmDialog from './ConfirmDialog'
import { useSnackbar } from './Snackbar'

function TestDashboard({ apiBase }) {
    const [selectedOperation, setSelectedOperation] = useState(null)
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [showProgress, setShowProgress] = useState(false)
    const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, type: null })
    const { showSuccess, showError, showInfo } = useSnackbar()

    const operations = {
        insert: {
            icon: '➕',
            color: '#10b981',
            methods: ['insert_one', 'insert_many', 'insert', 'save']
        },
        find: {
            icon: '🔍',
            color: '#3b82f6',
            methods: ['find', 'find_one', 'find_one_and_delete', 'find_one_and_replace', 'find_one_and_update', 'find_and_modify']
        },
        update: {
            icon: '✏️',
            color: '#f59e0b',
            methods: ['update_one', 'update_many', 'update', 'replace_one']
        },
        delete: {
            icon: '🗑️',
            color: '#ef4444',
            methods: ['delete_one', 'delete_many', 'remove']
        },
        count: {
            icon: '🔢',
            color: '#8b5cf6',
            methods: ['count', 'count_documents', 'estimated_document_count']
        },
        aggregation: {
            icon: '📊',
            color: '#ec4899',
            methods: ['aggregate', 'group', 'map_reduce', 'inline_map_reduce']
        },
        index: {
            icon: '🔑',
            color: '#14b8a6',
            methods: ['create_index', 'create_indexes', 'ensure_index', 'drop_index', 'drop_indexes', 'reindex']
        },
        collection: {
            icon: '📦',
            color: '#f97316',
            methods: ['distinct', 'rename', 'drop']
        },
        bulk: {
            icon: '⚡',
            color: '#6366f1',
            methods: ['bulk_write']
        }
    }

    const handleOperationClick = (operation) => {
        setSelectedOperation(operation)
        setResult(null)
    }

    const handleExecute = async (operation, data) => {
        setLoading(true)
        setResult(null)

        try {
            const startTime = performance.now()
            const response = await axios.post(`${apiBase}/api/${operation}`, data)
            const endTime = performance.now()

            setResult({
                success: response.data.success,
                data: response.data.data,
                error: response.data.error,
                executionTime: (endTime - startTime).toFixed(2),
                operation
            })
        } catch (error) {
            setResult({
                success: false,
                error: error.response?.data?.error || error.message,
                operation
            })
        } finally {
            setLoading(false)
        }
    }

    // Show confirm dialog for clear
    const showClearConfirm = () => {
        setConfirmDialog({
            isOpen: true,
            type: 'clear',
            title: 'Clear Collection',
            message: 'This will delete all documents from the test collection. This action cannot be undone.',
            confirmText: 'Clear All',
            confirmVariant: 'danger'
        })
    }

    // Show confirm dialog for run all
    const showRunAllConfirm = () => {
        setConfirmDialog({
            isOpen: true,
            type: 'runAll',
            title: 'Run All Operations',
            message: 'Execute all 35 MongoDB operations with complex sample data. Progress will be shown in real-time.',
            confirmText: 'Start Execution',
            confirmVariant: 'primary'
        })
    }

    // Handle confirm dialog actions
    const handleConfirm = async () => {
        const type = confirmDialog.type
        setConfirmDialog({ isOpen: false, type: null })

        if (type === 'clear') {
            await executeClear()
        } else if (type === 'runAll') {
            await executeRunAll()
        }
    }

    const executeClear = async () => {
        setLoading(true)
        try {
            const response = await axios.post(`${apiBase}/api/clear`)
            showSuccess(`Cleared ${response.data.data.deleted_count} documents`)
        } catch (error) {
            showError('Failed to clear: ' + error.message)
        } finally {
            setLoading(false)
        }
    }

    const executeRunAll = async () => {
        // Show modal immediately
        setShowProgress(true)
        setLoading(true)
        setResult(null)

        // Small delay to ensure modal renders before API call
        await new Promise(resolve => setTimeout(resolve, 100))

        try {
            const startTime = performance.now()
            const response = await axios.post(`${apiBase}/api/run_all`)
            const endTime = performance.now()

            const { summary } = response.data
            setResult({
                success: true,
                runAll: true,
                summary: summary,
                results: response.data.results,
                executionTime: (endTime - startTime).toFixed(2),
                operation: 'run_all'
            })
            showSuccess(`Completed! ${summary.successful}/${summary.total_operations} operations succeeded`)
        } catch (error) {
            setResult({
                success: false,
                error: error.response?.data?.error || error.message,
                operation: 'run_all'
            })
            showError('Run All failed: ' + (error.response?.data?.error || error.message))
        } finally {
            setLoading(false)
            // Don't close modal - let user close it manually
        }
    }

    return (
        <div>
            <div className="card">
                <div className="flex-between mb-2">
                    <h2>🚀 MongoDB Operations (35 Methods)</h2>
                <div className="flex gap-2">
                        <button
                            className="btn btn-primary"
                            onClick={showRunAllConfirm}
                            disabled={loading}
                        >
                            {loading ? '⏳ Running...' : '⚡ Run All Methods'}
                        </button>
                        <button
                            className="btn btn-danger"
                            onClick={showClearConfirm}
                            disabled={loading}
                        >
                            Clear Collection
                        </button>
                    </div>
                </div>

                {Object.entries(operations).map(([category, { icon, color, methods }]) => (
                    <div key={category} className="category">
                        <div className="category-header">
                            <span className="category-icon">{icon}</span>
                            <h3 style={{ color }}>{category.charAt(0).toUpperCase() + category.slice(1)}</h3>
                            <span className="text-muted">({methods.length} methods)</span>
                        </div>

                        <div className="grid grid-3">
                            {methods.map((method) => (
                                <div
                                    key={method}
                                    className="operation-card"
                                    onClick={() => handleOperationClick(method)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <div className="operation-name">{method}()</div>
                                    <button
                                        className="btn btn-primary"
                                        style={{ width: '100%' }}
                                        disabled={loading}
                                    >
                                        Execute
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {selectedOperation && (
                <TestRunner
                    operation={selectedOperation}
                    onExecute={handleExecute}
                    loading={loading}
                    onClose={() => setSelectedOperation(null)}
                />
            )}

            {result && (
                <ResultsDisplay result={result} />
            )}

            {showProgress && (
                <ProgressModal onClose={() => setShowProgress(false)} />
            )}

            <ConfirmDialog
                isOpen={confirmDialog.isOpen}
                title={confirmDialog.title}
                message={confirmDialog.message}
                confirmText={confirmDialog.confirmText}
                confirmVariant={confirmDialog.confirmVariant}
                onConfirm={handleConfirm}
                onCancel={() => setConfirmDialog({ isOpen: false, type: null })}
            />
        </div>
    )
}

export default TestDashboard

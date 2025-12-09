import React, { useState, useEffect, createContext, useContext, useCallback } from 'react'

// Create context for snackbar
const SnackbarContext = createContext()

// Snackbar types
const TYPES = {
    success: { bg: 'var(--accent-success)', icon: '✅' },
    error: { bg: 'var(--accent-error)', icon: '❌' },
    warning: { bg: 'var(--accent-warning)', icon: '⚠️' },
    info: { bg: 'var(--accent-primary)', icon: 'ℹ️' }
}

// Single Snackbar Item
function SnackbarItem({ message, type, id, onClose }) {
    useEffect(() => {
        const timer = setTimeout(() => onClose(id), 4000)
        return () => clearTimeout(timer)
    }, [id, onClose])

    const config = TYPES[type] || TYPES.info

    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '1rem 1.5rem',
            background: 'var(--bg-secondary)',
            borderLeft: `4px solid ${config.bg}`,
            borderRadius: '8px',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            animation: 'slideIn 0.3s ease',
            minWidth: '300px',
            maxWidth: '500px'
        }}>
            <span style={{ fontSize: '1.25rem' }}>{config.icon}</span>
            <span style={{ flex: 1, color: 'var(--text-primary)' }}>{message}</span>
            <button
                onClick={() => onClose(id)}
                style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--text-muted)',
                    cursor: 'pointer',
                    fontSize: '1.25rem',
                    padding: '0.25rem'
                }}
            >
                ×
            </button>
        </div>
    )
}

// Snackbar Container
function SnackbarContainer({ snackbars, removeSnackbar }) {
    if (snackbars.length === 0) return null

    return (
        <div style={{
            position: 'fixed',
            bottom: '2rem',
            right: '2rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem',
            zIndex: 2000
        }}>
            <style>{`
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `}</style>
            {snackbars.map(snack => (
                <SnackbarItem
                    key={snack.id}
                    {...snack}
                    onClose={removeSnackbar}
                />
            ))}
        </div>
    )
}

// Provider component
export function SnackbarProvider({ children }) {
    const [snackbars, setSnackbars] = useState([])

    const addSnackbar = useCallback((message, type = 'info') => {
        const id = Date.now()
        setSnackbars(prev => [...prev, { id, message, type }])
    }, [])

    const removeSnackbar = useCallback((id) => {
        setSnackbars(prev => prev.filter(s => s.id !== id))
    }, [])

    const showSuccess = useCallback((msg) => addSnackbar(msg, 'success'), [addSnackbar])
    const showError = useCallback((msg) => addSnackbar(msg, 'error'), [addSnackbar])
    const showWarning = useCallback((msg) => addSnackbar(msg, 'warning'), [addSnackbar])
    const showInfo = useCallback((msg) => addSnackbar(msg, 'info'), [addSnackbar])

    return (
        <SnackbarContext.Provider value={{ showSuccess, showError, showWarning, showInfo }}>
            {children}
            <SnackbarContainer snackbars={snackbars} removeSnackbar={removeSnackbar} />
        </SnackbarContext.Provider>
    )
}

// Hook to use snackbar
export function useSnackbar() {
    const context = useContext(SnackbarContext)
    if (!context) {
        throw new Error('useSnackbar must be used within SnackbarProvider')
    }
    return context
}

export default SnackbarProvider

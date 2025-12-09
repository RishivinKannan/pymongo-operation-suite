import React from 'react'

function ConfirmDialog({ 
    isOpen, 
    title = 'Confirm Action',
    message,
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    confirmVariant = 'primary', // primary, danger, warning
    onConfirm,
    onCancel
}) {
    if (!isOpen) return null

    const variantStyles = {
        primary: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)',
        danger: 'var(--accent-error)',
        warning: 'var(--accent-warning)'
    }

    return (
        <div className="modal-overlay" onClick={onCancel}>
            <div 
                className="modal" 
                onClick={e => e.stopPropagation()}
                style={{ maxWidth: '450px', textAlign: 'center' }}
            >
                <div style={{ marginBottom: '1.5rem' }}>
                    <div style={{ 
                        fontSize: '3rem', 
                        marginBottom: '1rem' 
                    }}>
                        {confirmVariant === 'danger' ? '⚠️' : 
                         confirmVariant === 'warning' ? '❓' : '🚀'}
                    </div>
                    <h2 style={{ marginBottom: '0.75rem' }}>{title}</h2>
                    <p style={{ 
                        color: 'var(--text-secondary)',
                        fontSize: '0.95rem',
                        lineHeight: '1.6'
                    }}>
                        {message}
                    </p>
                </div>

                <div style={{ 
                    display: 'flex', 
                    gap: '1rem', 
                    justifyContent: 'center' 
                }}>
                    <button 
                        className="btn btn-secondary" 
                        onClick={onCancel}
                    >
                        {cancelText}
                    </button>
                    <button 
                        className="btn"
                        style={{ background: variantStyles[confirmVariant] }}
                        onClick={onConfirm}
                    >
                        {confirmText}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmDialog

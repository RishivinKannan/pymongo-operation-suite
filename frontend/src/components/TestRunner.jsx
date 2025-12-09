import React, { useState } from 'react'

function TestRunner({ operation, onExecute, loading, onClose }) {
    const [formData, setFormData] = useState({})

    // Get form fields based on operation type
    const getFormFields = () => {
        const baseFields = {
            // Insert operations
            insert_one: [{ name: 'document', type: 'json', label: 'Document', default: '{"name": "John Doe", "age": 30, "email": "john@example.com"}' }],
            insert_many: [{ name: 'documents', type: 'json', label: 'Documents Array', default: '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]' }],
            insert: [{ name: 'documents', type: 'json', label: 'Document(s)', default: '{"name": "Test User", "status": "active"}' }],
            save: [{ name: 'document', type: 'json', label: 'Document', default: '{"name": "Saved User", "status": "active"}' }],

            // Find operations
            find: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{}' },
                { name: 'projection', type: 'json', label: 'Projection (optional)', default: '{}' },
                { name: 'limit', type: 'number', label: 'Limit', default: '10' }
            ],
            find_one: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{}' },
                { name: 'projection', type: 'json', label: 'Projection (optional)', default: '{}' }
            ],
            find_one_and_delete: [{ name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' }],
            find_one_and_replace: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' },
                { name: 'replacement', type: 'json', label: 'Replacement Document', default: '{"name": "Jane Doe", "age": 28}' }
            ],
            find_one_and_update: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' },
                { name: 'update', type: 'json', label: 'Update Document', default: '{"$set": {"age": 31}}' }
            ],
            find_and_modify: [
                { name: 'query', type: 'json', label: 'Query', default: '{"name": "John Doe"}' },
                { name: 'update', type: 'json', label: 'Update', default: '{"$set": {"status": "modified"}}' }
            ],

            // Update operations
            update_one: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' },
                { name: 'update', type: 'json', label: 'Update Document', default: '{"$set": {"age": 31}}' }
            ],
            update_many: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{"status": "active"}' },
                { name: 'update', type: 'json', label: 'Update Document', default: '{"$set": {"updated": true}}' }
            ],
            update: [
                { name: 'spec', type: 'json', label: 'Spec', default: '{"name": "John Doe"}' },
                { name: 'document', type: 'json', label: 'Document', default: '{"$set": {"age": 32}}' }
            ],
            replace_one: [
                { name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' },
                { name: 'replacement', type: 'json', label: 'Replacement Document', default: '{"name": "John Smith", "age": 30}' }
            ],

            // Delete operations
            delete_one: [{ name: 'filter', type: 'json', label: 'Filter Query', default: '{"name": "John Doe"}' }],
            delete_many: [{ name: 'filter', type: 'json', label: 'Filter Query', default: '{"status": "inactive"}' }],
            remove: [{ name: 'spec', type: 'json', label: 'Spec', default: '{"name": "John Doe"}' }],

            // Count operations
            count: [{ name: 'filter', type: 'json', label: 'Filter Query (optional)', default: '{}' }],
            count_documents: [{ name: 'filter', type: 'json', label: 'Filter Query (optional)', default: '{}' }],
            estimated_document_count: [],

            // Aggregation operations
            aggregate: [{ name: 'pipeline', type: 'json', label: 'Aggregation Pipeline', default: '[{"$match": {"age": {"$gte": 25}}}, {"$group": {"_id": "$status", "count": {"$sum": 1}}}]' }],
            group: [
                { name: 'key', type: 'json', label: 'Key', default: '{"status": 1}' },
                { name: 'condition', type: 'json', label: 'Condition', default: '{}' },
                { name: 'initial', type: 'json', label: 'Initial', default: '{"count": 0}' },
                { name: 'reduce', type: 'text', label: 'Reduce Function', default: 'function(obj, prev) { prev.count++; }' }
            ],
            map_reduce: [
                { name: 'map', type: 'text', label: 'Map Function', default: 'function() { emit(this.status, 1); }' },
                { name: 'reduce', type: 'text', label: 'Reduce Function', default: 'function(key, values) { return Array.sum(values); }' },
                { name: 'out', type: 'text', label: 'Output Collection', default: 'mr_results' }
            ],
            inline_map_reduce: [
                { name: 'map', type: 'text', label: 'Map Function', default: 'function() { emit(this.status, 1); }' },
                { name: 'reduce', type: 'text', label: 'Reduce Function', default: 'function(key, values) { return Array.sum(values); }' }
            ],

            // Index operations
            create_index: [
                { name: 'field', type: 'text', label: 'Field Name', default: 'email' },
                { name: 'direction', type: 'number', label: 'Direction (1/-1)', default: '1' },
                { name: 'unique', type: 'checkbox', label: 'Unique', default: false }
            ],
            create_indexes: [{ name: 'indexes', type: 'json', label: 'Indexes Array', default: '[{"field": "email", "direction": 1}, {"field": "name", "direction": 1}]' }],
            ensure_index: [
                { name: 'field', type: 'text', label: 'Field Name', default: 'email' },
                { name: 'direction', type: 'number', label: 'Direction (1/-1)', default: '1' }
            ],
            drop_index: [{ name: 'index_name', type: 'text', label: 'Index Name', default: 'email_1' }],
            drop_indexes: [],
            reindex: [],

            // Collection operations
            distinct: [
                { name: 'key', type: 'text', label: 'Field Name', default: 'status' },
                { name: 'filter', type: 'json', label: 'Filter Query (optional)', default: '{}' }
            ],
            rename: [{ name: 'new_name', type: 'text', label: 'New Collection Name', default: 'test_collection_renamed' }],
            drop: [],

            // Bulk operations
            bulk_write: [{
                name: 'operations',
                type: 'json',
                label: 'Operations Array',
                default: '[{"type": "insert", "document": {"name": "Bulk User 1"}}, {"type": "update", "filter": {"name": "John Doe"}, "update": {"$set": {"bulk": true}}}]'
            }]
        }

        return baseFields[operation] || []
    }

    const handleSubmit = (e) => {
        e.preventDefault()

        // Parse JSON fields
        const parsedData = {}
        const fields = getFormFields()

        fields.forEach(field => {
            const value = formData[field.name] !== undefined ? formData[field.name] : field.default

            if (field.type === 'json') {
                try {
                    parsedData[field.name] = JSON.parse(value || '{}')
                } catch (err) {
                    alert(`Invalid JSON in ${field.label}: ${err.message}`)
                    return
                }
            } else if (field.type === 'number') {
                parsedData[field.name] = parseInt(value) || 0
            } else if (field.type === 'checkbox') {
                parsedData[field.name] = value === true || value === 'true'
            } else {
                parsedData[field.name] = value
            }
        })

        onExecute(operation, parsedData)
    }

    const fields = getFormFields()

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="flex-between mb-2">
                    <h2>Execute: {operation}()</h2>
                    <button className="btn btn-secondary" onClick={onClose}>✕ Close</button>
                </div>

                <form onSubmit={handleSubmit}>
                    {fields.length === 0 ? (
                        <p className="text-muted mb-2">This operation requires no parameters.</p>
                    ) : (
                        fields.map((field) => (
                            <div key={field.name} className="input-group">
                                <label className="input-label">{field.label}</label>
                                {field.type === 'json' || field.type === 'text' ? (
                                    <textarea
                                        className="textarea-field"
                                        defaultValue={field.default}
                                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                                        placeholder={field.label}
                                    />
                                ) : field.type === 'number' ? (
                                    <input
                                        type="number"
                                        className="input-field"
                                        defaultValue={field.default}
                                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                                    />
                                ) : field.type === 'checkbox' ? (
                                    <input
                                        type="checkbox"
                                        defaultChecked={field.default}
                                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked })}
                                    />
                                ) : null}
                            </div>
                        ))
                    )}

                    <div className="flex gap-2 mt-2">
                        <button
                            type="submit"
                            className="btn btn-success"
                            disabled={loading}
                            style={{ flex: 1 }}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    <span>Executing...</span>
                                </>
                            ) : (
                                <>
                                    <span>▶️</span>
                                    <span>Execute Operation</span>
                                </>
                            )}
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={onClose}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default TestRunner

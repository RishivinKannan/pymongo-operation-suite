"""
Flask REST API for PyMongo Testing
Provides endpoints for all 35 MongoDB Collection operations
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pymongo import IndexModel, ASCENDING, DESCENDING
from pymongo import InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne, UpdateMany
from dotenv import load_dotenv

from observability import initialize_observability
from database import MongoDBOperations

import atatus

# Load environment variables
load_dotenv()

# Initialize observability

# Create Flask app with static file serving
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
observability_status = initialize_observability(app)
CORS(app)  # Enable CORS for frontend

atatus_client = atatus.get_client()
# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize MongoDB operations
db_ops = MongoDBOperations()

# Connect to MongoDB on startup
@app.before_request
def before_first_request():
    """Initialize database connection"""
    if not db_ops.client:
        db_ops.connect()


# ========== HEALTH & STATUS ==========

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "observability": {
            "opentelemetry": "enabled",
            "datadog": observability_status.get('datadog', False),
            "atatus": observability_status.get('atatus', False)
        }
    })

@app.route('/')
def serve_index():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    """Serve index.html for client-side routing (SPA)"""
    # Only serve index.html for non-API routes
    if not request.path.startswith('/api/'):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({"error": "Not found"}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get collection statistics"""
    try:
        stats = db_ops.get_collection_stats()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== INSERT OPERATIONS ==========

@app.route('/api/insert_one', methods=['POST'])
def api_insert_one():
    """Insert a single document"""
    try:
        data = request.get_json()
        document = data.get('document', {})
        result = db_ops.insert_one(document)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/insert_many', methods=['POST'])
def api_insert_many():
    """Insert multiple documents"""
    try:
        data = request.get_json()
        documents = data.get('documents', [])
        result = db_ops.insert_many(documents)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/insert', methods=['POST'])
def api_insert():
    """Deprecated insert method"""
    try:
        data = request.get_json()
        # Handle both single document and multiple documents
        doc_or_docs = data.get('documents') or data.get('document')
        if doc_or_docs is None:
            return jsonify({"success": False, "error": "Missing 'document' or 'documents' field"}), 400
        result = db_ops.insert(doc_or_docs)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/save', methods=['POST'])
def api_save():
    """Deprecated save method"""
    try:
        data = request.get_json()
        document = data.get('document', {})
        result = db_ops.save(document)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== FIND OPERATIONS ==========

@app.route('/api/find', methods=['POST'])
def api_find():
    """Find multiple documents"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        projection = data.get('projection')
        limit = data.get('limit', 10)
        result = db_ops.find(filter_query, projection, limit)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/find_one', methods=['POST'])
def api_find_one():
    """Find a single document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        projection = data.get('projection')
        result = db_ops.find_one(filter_query, projection)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/find_one_and_delete', methods=['POST'])
def api_find_one_and_delete():
    """Find and delete a document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        result = db_ops.find_one_and_delete(filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/find_one_and_replace', methods=['POST'])
def api_find_one_and_replace():
    """Find and replace a document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        replacement = data.get('replacement', {})
        result = db_ops.find_one_and_replace(filter_query, replacement)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/find_one_and_update', methods=['POST'])
def api_find_one_and_update():
    """Find and update a document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        update = data.get('update', {})
        result = db_ops.find_one_and_update(filter_query, update)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/find_and_modify', methods=['POST'])
def api_find_and_modify():
    """Deprecated find and modify"""
    try:
        data = request.get_json()
        query = data.get('query', {})
        update = data.get('update')
        remove = data.get('remove', False)
        result = db_ops.find_and_modify(query, update, remove)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== UPDATE OPERATIONS ==========

@app.route('/api/update_one', methods=['POST'])
def api_update_one():
    """Update a single document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        update = data.get('update', {})
        result = db_ops.update_one(filter_query, update)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/update_many', methods=['POST'])
def api_update_many():
    """Update multiple documents"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        update = data.get('update', {})
        result = db_ops.update_many(filter_query, update)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/update', methods=['POST'])
def api_update():
    """Deprecated update method"""
    try:
        data = request.get_json()
        spec = data.get('spec', {})
        document = data.get('document', {})
        multi = data.get('multi', False)
        result = db_ops.update(spec, document, multi)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/replace_one', methods=['POST'])
def api_replace_one():
    """Replace a single document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        replacement = data.get('replacement', {})
        result = db_ops.replace_one(filter_query, replacement)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== DELETE OPERATIONS ==========

@app.route('/api/delete_one', methods=['POST'])
def api_delete_one():
    """Delete a single document"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        result = db_ops.delete_one(filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/delete_many', methods=['POST'])
def api_delete_many():
    """Delete multiple documents"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        result = db_ops.delete_many(filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/remove', methods=['POST'])
def api_remove():
    """Deprecated remove method"""
    try:
        data = request.get_json()
        spec = data.get('spec', {})
        multi = data.get('multi', False)
        result = db_ops.remove(spec, multi)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== COUNT OPERATIONS ==========

@app.route('/api/count', methods=['POST'])
def api_count():
    """Deprecated count method"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        result = db_ops.count(filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/count_documents', methods=['POST'])
def api_count_documents():
    """Count documents"""
    try:
        data = request.get_json()
        filter_query = data.get('filter', {})
        result = db_ops.count_documents(filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/estimated_document_count', methods=['GET'])
def api_estimated_document_count():
    """Get estimated document count"""
    try:
        result = db_ops.estimated_document_count()
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== AGGREGATION OPERATIONS ==========

@app.route('/api/aggregate', methods=['POST'])
def api_aggregate():
    """Execute aggregation pipeline"""
    try:
        data = request.get_json()
        pipeline = data.get('pipeline', [])
        result = db_ops.aggregate(pipeline)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/group', methods=['POST'])
def api_group():
    """Deprecated group method"""
    try:
        data = request.get_json()
        key = data.get('key')
        condition = data.get('condition', {})
        initial = data.get('initial', {})
        reduce = data.get('reduce', '')
        result = db_ops.group(key, condition, initial, reduce)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/map_reduce', methods=['POST'])
def api_map_reduce():
    """Execute map-reduce"""
    try:
        data = request.get_json()
        map_func = data.get('map', '')
        reduce_func = data.get('reduce', '')
        out = data.get('out', 'mr_results')
        result = db_ops.map_reduce(map_func, reduce_func, out)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/inline_map_reduce', methods=['POST'])
def api_inline_map_reduce():
    """Execute inline map-reduce"""
    try:
        data = request.get_json()
        map_func = data.get('map', '')
        reduce_func = data.get('reduce', '')
        result = db_ops.inline_map_reduce(map_func, reduce_func)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== INDEX OPERATIONS ==========

@app.route('/api/create_index', methods=['POST'])
def api_create_index():
    """Create an index"""
    try:
        data = request.get_json()
        field = data.get('field', 'name')  # Default field
        direction = data.get('direction', 1)  # 1 for ascending, -1 for descending
        unique = data.get('unique', False)
        result = db_ops.create_index([(field, direction)], unique=unique)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/create_indexes', methods=['POST'])
def api_create_indexes():
    """Create multiple indexes"""
    try:
        data = request.get_json()
        indexes_spec = data.get('indexes', [])
        # Convert to IndexModel objects - handle multiple formats
        indexes = []
        for spec in indexes_spec:
            if isinstance(spec, dict) and 'keys' in spec:
                # Format: {"keys": [["field", 1], ["field2", -1]]}
                keys = [(k[0], k[1]) for k in spec['keys']]
                indexes.append(IndexModel(keys))
            elif isinstance(spec, list):
                # Format: [["field", 1], ["field2", -1]] - tuple list
                if spec and isinstance(spec[0], list):
                    keys = [(k[0], k[1]) for k in spec]
                    indexes.append(IndexModel(keys))
                else:
                    # Single key: ["field", 1]
                    indexes.append(IndexModel([(spec[0], spec[1])]))
            elif isinstance(spec, dict) and 'field' in spec:
                # Legacy format: {"field": "name", "direction": 1}
                indexes.append(IndexModel([(spec['field'], spec.get('direction', 1))]))
        
        if not indexes:
            return jsonify({"success": False, "error": "No valid index specifications"}), 400
            
        result = db_ops.create_indexes(indexes)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ensure_index', methods=['POST'])
def api_ensure_index():
    """Deprecated ensure index"""
    try:
        data = request.get_json()
        field = data.get('field', 'name')
        direction = data.get('direction', 1)
        result = db_ops.ensure_index([(field, direction)])
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/drop_index', methods=['POST'])
def api_drop_index():
    """Drop an index"""
    try:
        data = request.get_json()
        index_name = data.get('index_name')
        result = db_ops.drop_index(index_name)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/drop_indexes', methods=['POST'])
def api_drop_indexes():
    """Drop all indexes"""
    try:
        result = db_ops.drop_indexes()
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reindex', methods=['POST'])
def api_reindex():
    """Reindex collection"""
    try:
        result = db_ops.reindex()
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== COLLECTION OPERATIONS ==========

@app.route('/api/distinct', methods=['POST'])
def api_distinct():
    """Get distinct values"""
    try:
        data = request.get_json()
        key = data.get('key', 'name')
        filter_query = data.get('filter', {})
        result = db_ops.distinct(key, filter_query)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/rename', methods=['POST'])
def api_rename():
    """Rename collection"""
    try:
        data = request.get_json()
        new_name = data.get('new_name')
        result = db_ops.rename(new_name)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/drop', methods=['POST'])
def api_drop():
    """Drop collection"""
    try:
        result = db_ops.drop()
        # Recreate collection
        db_ops.collection = db_ops.db['test_collection']
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== BULK OPERATIONS ==========

@app.route('/api/bulk_write', methods=['POST'])
def api_bulk_write():
    """Execute bulk write operations"""
    try:
        data = request.get_json()
        operations = data.get('operations', [])
        
        # Convert operation specs to pymongo operation objects
        bulk_ops = []
        for op in operations:
            # Handle MongoDB-style format (insertOne, updateOne, etc)
            if 'insertOne' in op:
                doc = op['insertOne'].get('document', op['insertOne'])
                bulk_ops.append(InsertOne(doc))
            elif 'updateOne' in op:
                bulk_ops.append(UpdateOne(op['updateOne']['filter'], op['updateOne']['update']))
            elif 'updateMany' in op:
                bulk_ops.append(UpdateMany(op['updateMany']['filter'], op['updateMany']['update']))
            elif 'deleteOne' in op:
                bulk_ops.append(DeleteOne(op['deleteOne']['filter']))
            elif 'deleteMany' in op:
                bulk_ops.append(DeleteMany(op['deleteMany']['filter']))
            elif 'replaceOne' in op:
                bulk_ops.append(ReplaceOne(op['replaceOne']['filter'], op['replaceOne']['replacement']))
            # Legacy format support
            elif op.get('type') == 'insert':
                bulk_ops.append(InsertOne(op['document']))
            elif op.get('type') == 'update':
                bulk_ops.append(UpdateOne(op['filter'], op['update']))
            elif op.get('type') == 'delete':
                bulk_ops.append(DeleteOne(op['filter']))
            elif op.get('type') == 'replace':
                bulk_ops.append(ReplaceOne(op['filter'], op['replacement']))
        
        if not bulk_ops:
            return jsonify({"success": False, "error": "No valid operations to execute"}), 400
            
        result = db_ops.bulk_write(bulk_ops)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== UTILITY ENDPOINTS ==========

@app.route('/api/clear', methods=['POST'])
def api_clear():
    """Clear all documents from collection"""
    try:
        result = db_ops.clear_collection()
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/operations', methods=['GET'])
def list_operations():
    """List all available operations"""
    operations = {
        "insert": ["insert_one", "insert_many", "insert", "save"],
        "find": ["find", "find_one", "find_one_and_delete", "find_one_and_replace", "find_one_and_update", "find_and_modify"],
        "update": ["update_one", "update_many", "update", "replace_one"],
        "delete": ["delete_one", "delete_many", "remove"],
        "count": ["count", "count_documents", "estimated_document_count"],
        "aggregation": ["aggregate", "group", "map_reduce", "inline_map_reduce"],
        "index": ["create_index", "create_indexes", "ensure_index", "drop_index", "drop_indexes", "reindex"],
        "collection": ["distinct", "rename", "drop"],
        "bulk": ["bulk_write"]
    }
    return jsonify({"success": True, "operations": operations, "total": 35})


@app.route('/api/run_all', methods=['POST'])
def run_all_operations():
 # your transaction name
    # TODO: your operations
    """Execute all 35 operations concurrently by calling their API endpoints"""
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from threading import Lock
    
    results = []
    results_lock = Lock()
    start_time = time.time()
    
    # Clear collection first
    try:
        db_ops.clear_collection()
    except:
        pass
    
    # All 34 PyMongo Collection methods (including deprecated ones for PyMongo 3.x)
    test_operations = [
        # === 1. INSERT OPERATIONS (4 methods) ===
        ("insert_one", "/api/insert_one", {"document": {
            "name": "Alice Johnson", "age": 30, "email": "alice@example.com", "status": "active",
            "department": "Engineering", "salary": 85000, "tags": ["python", "mongodb"]
        }}),
        
        ("insert_many", "/api/insert_many", {"documents": [
            {"name": "Bob Smith", "age": 25, "email": "bob@example.com", "status": "active", "department": "Marketing", "salary": 65000},
            {"name": "Charlie Brown", "age": 35, "email": "charlie@example.com", "status": "inactive", "department": "Engineering", "salary": 95000},
            {"name": "Diana Ross", "age": 28, "email": "diana@example.com", "status": "active", "department": "Sales", "salary": 72000},
            {"name": "Edward Chen", "age": 42, "email": "edward@example.com", "status": "active", "department": "Engineering", "salary": 120000},
            {"name": "Fiona Garcia", "age": 31, "email": "fiona@example.com", "status": "active", "department": "HR", "salary": 68000}
        ]}),
        
        # DEPRECATED: insert (use insert_one/insert_many instead)
        ("insert", "/api/insert", {"document": {"name": "George Wilson", "age": 45, "department": "Finance", "salary": 110000}}),
        
        # DEPRECATED: save (use insert_one or replace_one instead)
        ("save", "/api/save", {"document": {"name": "Hannah Lee", "age": 33, "department": "Engineering", "salary": 92000}}),
        
        # === 2. FIND OPERATIONS (6 methods) ===
        ("find", "/api/find", {"filter": {"status": "active", "salary": {"$gte": 70000}}, "limit": 50}),
        
        ("find_one", "/api/find_one", {"filter": {"$or": [{"age": {"$gte": 40}}, {"salary": {"$gte": 100000}}]}}),
        
        ("find_one_and_delete", "/api/find_one_and_delete", {"filter": {"status": "inactive"}}),
        
        ("find_one_and_replace", "/api/find_one_and_replace", {"filter": {"email": "diana@example.com"}, "replacement": {
            "name": "Diana Ross-Smith", "age": 29, "email": "diana@example.com", "status": "active", "department": "Sales", "salary": 82000
        }}),
        
        ("find_one_and_update", "/api/find_one_and_update", {"filter": {"department": "Sales"}, "update": {"$set": {"last_activity": "2024-12-09"}}}),
        
        # DEPRECATED: find_and_modify (use find_one_and_update/replace/delete instead)
        ("find_and_modify", "/api/find_and_modify", {"filter": {"salary": {"$gte": 100000}}, "update": {"$set": {"high_earner": True}}}),
        
        # === 3. UPDATE OPERATIONS (4 methods) ===
        ("update_one", "/api/update_one", {"filter": {"name": "Alice Johnson"}, "update": {"$set": {"status": "senior"}, "$inc": {"salary": 15000}}}),
        
        ("update_many", "/api/update_many", {"filter": {"department": "Engineering"}, "update": {"$set": {"review_pending": True}}}),
        
        # DEPRECATED: update (use update_one/update_many instead)
        ("update", "/api/update", {"filter": {"name": "Bob Smith"}, "update": {"$set": {"address": "San Francisco"}}}),
        
        ("replace_one", "/api/replace_one", {"filter": {"name": "Fiona Garcia"}, "replacement": {
            "name": "Fiona Garcia", "age": 32, "department": "HR", "salary": 75000, "promoted": True
        }}),
        
        # === 4. DELETE OPERATIONS (3 methods) ===
        ("delete_one", "/api/delete_one", {"filter": {"status": "temporary"}}),
        
        ("delete_many", "/api/delete_many", {"filter": {"department": "Intern"}}),
        
        # DEPRECATED: remove (use delete_one/delete_many instead)
        ("remove", "/api/remove", {"filter": {"name": "NonExistent User"}}),
        
        # === 5. COUNT OPERATIONS (3 methods) ===
        ("count_documents", "/api/count_documents", {"filter": {"department": "Engineering"}}),
        
        ("estimated_document_count", "/api/estimated_document_count", {}),
        
        # DEPRECATED: count (use count_documents instead)
        ("count", "/api/count", {"filter": {"salary": {"$gte": 80000}}}),
        
        # === 6. AGGREGATION OPERATIONS (4 methods) ===
        ("aggregate", "/api/aggregate", {"pipeline": [
            {"$match": {"status": "active"}},
            {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}, "count": {"$sum": 1}}},
            {"$sort": {"avg_salary": -1}}
        ]}),
        
        # DEPRECATED: group (use aggregate with $group instead) - removed in MongoDB 5.0+
        # Skipping group as it's not supported in modern MongoDB versions
        
        # DEPRECATED: map_reduce (use aggregate instead)
        ("map_reduce", "/api/map_reduce", {
            "map": "function() { emit(this.department, this.salary); }",
            "reduce": "function(key, values) { return Array.sum(values); }",
            "out": "salary_by_dept"
        }),
        
        # DEPRECATED: inline_map_reduce (use aggregate instead)
        ("inline_map_reduce", "/api/inline_map_reduce", {
            "map": "function() { emit(this.department, 1); }",
            "reduce": "function(key, values) { return Array.sum(values); }"
        }),
        
        # === 7. INDEX OPERATIONS (6 methods) - ORDER MATTERS! ===
        # Create indexes FIRST
        ("create_index", "/api/create_index", {"keys": [["email", 1]]}),
        
        ("create_indexes", "/api/create_indexes", {"indexes": [
            {"keys": [["department", 1], ["salary", -1]]},
            {"keys": [["status", 1]]}
        ]}),
        
        # DEPRECATED: ensure_index (use create_index instead)
        ("ensure_index", "/api/ensure_index", {"keys": [["age", 1]]}),
        
        # DEPRECATED: reindex 
        ("reindex", "/api/reindex", {}),
        
        # Drop indexes AFTER creating them
        ("drop_index", "/api/drop_index", {"index_name": "email_1"}),
        
        ("drop_indexes", "/api/drop_indexes", {}),
        
        # === 8. COLLECTION OPERATIONS (2 methods) - MUST BE LAST ===
        ("distinct", "/api/distinct", {"field": "department"}),
        
        # Rename collection (must be at the end - changes collection name)
        ("rename", "/api/rename", {"new_name": "test_collection_backup"}),
        
        # === 9. BULK OPERATIONS (1 method) ===
        ("bulk_write", "/api/bulk_write", {
            "operations": [
                {"insertOne": {"document": {"name": "Bulk User 1", "age": 25, "department": "Temp"}}},
                {"updateOne": {"filter": {"name": "Bulk User 1"}, "update": {"$set": {"bulk_tested": True}}}},
                {"deleteOne": {"filter": {"name": "Bulk User 1"}}}
            ]
        }),
        
        # === 10. DROP COLLECTION (last - recreate collection for next run) ===
        ("drop", "/api/drop", {}),
    ]
    
    total_ops = len(test_operations)
    completed = 0
    
    # Emit start event
    socketio.emit('progress', {
        'type': 'start',
        'total': total_ops,
        'message': f'Starting sequential execution of {total_ops} operations...'
    })
    
    def execute_operation(index, op_name, endpoint, payload):
        """Execute a single operation by calling its API endpoint"""
        nonlocal completed
        op_start = time.time()
        
        # Emit start event
        socketio.emit('progress', {
            'type': 'operation_start',
            'operation': op_name,
            'current': index,
            'total': total_ops,
            'message': f'Executing {op_name}...'
        })
        
        try:
            # Make an HTTP request to the endpoint
            import requests as http_requests
            base_url = f"http://localhost:{os.getenv('FLASK_PORT', 5000)}"
            
            # Use GET for endpoints that require it
            if op_name == 'estimated_document_count':
                response = http_requests.get(f"{base_url}{endpoint}")
            else:
                response = http_requests.post(f"{base_url}{endpoint}", json=payload)
            result_data = response.json() if response.text else {}
                
            op_time = (time.time() - op_start) * 1000  # Convert to ms
            
            result_entry = {
                "operation": op_name,
                "success": response.status_code == 200,
                "result": result_data.get('result') if response.status_code == 200 else None,
                "execution_time_ms": round(op_time, 2)
            }
            
            if response.status_code != 200:
                result_entry["error"] = result_data.get('error', f'HTTP {response.status_code}')
            
            with results_lock:
                results.append(result_entry)
                completed += 1
            
            # Emit success/failure event
            socketio.emit('progress', {
                'type': 'operation_complete',
                'operation': op_name,
                'success': response.status_code == 200,
                'current': completed,
                'total': total_ops,
                'execution_time_ms': round(op_time, 2),
                'message': f'{"✓" if response.status_code == 200 else "✗"} {op_name} completed in {round(op_time, 0)}ms'
            })
            
            return result_entry
            
        except Exception as e:
            op_time = (time.time() - op_start) * 1000
            
            result_entry = {
                "operation": op_name,
                "success": False,
                "error": str(e),
                "execution_time_ms": round(op_time, 2)
            }
            
            with results_lock:
                results.append(result_entry)
                completed += 1
            
            # Emit error event
            socketio.emit('progress', {
                'type': 'operation_complete',
                'operation': op_name,
                'success': False,
                'current': completed,
                'total': total_ops,
                'execution_time_ms': round(op_time, 2),
                'error': str(e),
                'message': f'✗ {op_name} failed: {str(e)[:50]}'
            })
            
            return result_entry
    
    # Execute operations SEQUENTIALLY to avoid race conditions
    # (Index operations conflict when run concurrently)
    for index, (op_name, endpoint, payload) in enumerate(test_operations, 1):
        try:
            execute_operation(index, op_name, endpoint, payload)
        except Exception as e:
            print(f"Operation {op_name} failed with exception: {e}")
    
    total_time = (time.time() - start_time) * 1000
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    summary = {
        "total_operations": len(results),
        "successful": successful,
        "failed": failed,
        "total_time_ms": round(total_time, 2)
    }
    
    # Emit completion event
    socketio.emit('progress', {
        'type': 'complete',
        'summary': summary,
        'message': f'Completed! {successful}/{len(results)} operations succeeded in {round(total_time, 0)}ms'
    })
    
    return jsonify({
        "success": True,
        "summary": summary,
        "results": results
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print("\n🚀 Flask API Server Starting...")
    print(f"📍 API: http://localhost:{port}")
    print(f"📊 Jaeger UI: http://localhost:16686")
    print(f"🔧 Debug Mode: {debug}")
    print(f"🔌 WebSocket: Enabled\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)

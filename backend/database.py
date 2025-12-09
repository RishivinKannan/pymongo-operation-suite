"""
MongoDB Database Operations - All 35 PyMongo Collection Methods
Includes comprehensive implementation of all Collection methods with observability
"""
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from opentelemetry import trace

# Load environment variables
load_dotenv()

# Get tracer for manual instrumentation
tracer = trace.get_tracer(__name__)


class MongoDBOperations:
    """MongoDB operations handler with all 35 Collection methods"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/?replicaSet=rs0')
        self.db_name = os.getenv('MONGODB_DB_NAME', 'testdb')
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        with tracer.start_as_current_span("mongodb.connect"):
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db['test_collection']
            # Verify connection
            self.client.admin.command('ping')
            return {"status": "connected", "database": self.db_name}
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            return {"status": "disconnected"}
    
    # ========== INSERT OPERATIONS ==========
    
    def insert_one(self, document: Dict) -> Dict:
        """Insert a single document"""
        with tracer.start_as_current_span("collection.insert_one"):
            result = self.collection.insert_one(document)
            return {
                "operation": "insert_one",
                "inserted_id": str(result.inserted_id),
                "acknowledged": result.acknowledged
            }
    
    def insert_many(self, documents: List[Dict]) -> Dict:
        """Insert multiple documents"""
        with tracer.start_as_current_span("collection.insert_many"):
            result = self.collection.insert_many(documents)
            return {
                "operation": "insert_many",
                "inserted_ids": [str(id) for id in result.inserted_ids],
                "inserted_count": len(result.inserted_ids),
                "acknowledged": result.acknowledged
            }
    
    def insert(self, doc_or_docs) -> Dict:
        """Deprecated: Insert one or more documents (legacy method)"""
        with tracer.start_as_current_span("collection.insert"):
            result = self.collection.insert(doc_or_docs)
            if isinstance(result, list):
                return {
                    "operation": "insert",
                    "inserted_ids": [str(id) for id in result],
                    "count": len(result)
                }
            return {
                "operation": "insert",
                "inserted_id": str(result)
            }
    
    def save(self, document: Dict) -> Dict:
        """Deprecated: Save a document (insert or update)"""
        with tracer.start_as_current_span("collection.save"):
            result = self.collection.save(document)
            return {
                "operation": "save",
                "saved_id": str(result)
            }
    
    # ========== FIND OPERATIONS ==========
    
    def find(self, filter_query: Dict = None, projection: Dict = None, limit: int = 0) -> Dict:
        """Find multiple documents"""
        with tracer.start_as_current_span("collection.find"):
            filter_query = filter_query or {}
            cursor = self.collection.find(filter_query, projection).limit(limit)
            documents = list(cursor)
            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            return {
                "operation": "find",
                "count": len(documents),
                "documents": documents
            }
    
    def find_one(self, filter_query: Dict = None, projection: Dict = None) -> Dict:
        """Find a single document"""
        with tracer.start_as_current_span("collection.find_one"):
            filter_query = filter_query or {}
            document = self.collection.find_one(filter_query, projection)
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            return {
                "operation": "find_one",
                "document": document
            }
    
    def find_one_and_delete(self, filter_query: Dict) -> Dict:
        """Find a single document and delete it"""
        with tracer.start_as_current_span("collection.find_one_and_delete"):
            document = self.collection.find_one_and_delete(filter_query)
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            return {
                "operation": "find_one_and_delete",
                "deleted_document": document
            }
    
    def find_one_and_replace(self, filter_query: Dict, replacement: Dict) -> Dict:
        """Find a single document and replace it"""
        with tracer.start_as_current_span("collection.find_one_and_replace"):
            document = self.collection.find_one_and_replace(filter_query, replacement)
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            return {
                "operation": "find_one_and_replace",
                "old_document": document
            }
    
    def find_one_and_update(self, filter_query: Dict, update: Dict) -> Dict:
        """Find a single document and update it"""
        with tracer.start_as_current_span("collection.find_one_and_update"):
            document = self.collection.find_one_and_update(filter_query, update)
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            return {
                "operation": "find_one_and_update",
                "old_document": document
            }
    
    def find_and_modify(self, query: Dict, update: Dict = None, remove: bool = False) -> Dict:
        """Deprecated: Find and modify a document"""
        with tracer.start_as_current_span("collection.find_and_modify"):
            document = self.collection.find_and_modify(query=query, update=update, remove=remove)
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            return {
                "operation": "find_and_modify",
                "document": document
            }
    
    # ========== UPDATE OPERATIONS ==========
    
    def update_one(self, filter_query: Dict, update: Dict) -> Dict:
        """Update a single document"""
        with tracer.start_as_current_span("collection.update_one"):
            result = self.collection.update_one(filter_query, update)
            return {
                "operation": "update_one",
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }
    
    def update_many(self, filter_query: Dict, update: Dict) -> Dict:
        """Update multiple documents"""
        with tracer.start_as_current_span("collection.update_many"):
            result = self.collection.update_many(filter_query, update)
            return {
                "operation": "update_many",
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }
    
    def update(self, spec: Dict, document: Dict, multi: bool = False) -> Dict:
        """Deprecated: Update documents"""
        with tracer.start_as_current_span("collection.update"):
            result = self.collection.update(spec, document, multi=multi)
            return {
                "operation": "update",
                "result": result
            }
    
    def replace_one(self, filter_query: Dict, replacement: Dict) -> Dict:
        """Replace a single document"""
        with tracer.start_as_current_span("collection.replace_one"):
            result = self.collection.replace_one(filter_query, replacement)
            return {
                "operation": "replace_one",
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }
    
    # ===== DELETE OPERATIONS ==========
    
    def delete_one(self, filter_query: Dict) -> Dict:
        """Delete a single document"""
        with tracer.start_as_current_span("collection.delete_one"):
            result = self.collection.delete_one(filter_query)
            return {
                "operation": "delete_one",
                "deleted_count": result.deleted_count,
                "acknowledged": result.acknowledged
            }
    
    def delete_many(self, filter_query: Dict) -> Dict:
        """Delete multiple documents"""
        with tracer.start_as_current_span("collection.delete_many"):
            result = self.collection.delete_many(filter_query)
            return {
                "operation": "delete_many",
                "deleted_count": result.deleted_count,
                "acknowledged": result.acknowledged
            }
    
    def remove(self, spec_or_id: Dict, multi: bool = False) -> Dict:
        """Deprecated: Remove documents"""
        with tracer.start_as_current_span("collection.remove"):
            result = self.collection.remove(spec_or_id, multi=multi)
            return {
                "operation": "remove",
                "result": result
            }
    
    # ========== COUNT OPERATIONS ==========
    
    def count(self, filter_query: Dict = None) -> Dict:
        """Deprecated: Count documents (use count_documents instead)"""
        with tracer.start_as_current_span("collection.count"):
            filter_query = filter_query or {}
            count = self.collection.count(filter_query)
            return {
                "operation": "count",
                "count": count
            }
    
    def count_documents(self, filter_query: Dict = None) -> Dict:
        """Count documents matching a query"""
        with tracer.start_as_current_span("collection.count_documents"):
            filter_query = filter_query or {}
            count = self.collection.count_documents(filter_query)
            return {
                "operation": "count_documents",
                "count": count
            }
    
    def estimated_document_count(self) -> Dict:
        """Get estimated total document count"""
        with tracer.start_as_current_span("collection.estimated_document_count"):
            count = self.collection.estimated_document_count()
            return {
                "operation": "estimated_document_count",
                "count": count
            }
    
    # ========== AGGREGATION OPERATIONS ==========
    
    def aggregate(self, pipeline: List[Dict]) -> Dict:
        """Execute an aggregation pipeline"""
        with tracer.start_as_current_span("collection.aggregate"):
            cursor = self.collection.aggregate(pipeline)
            results = list(cursor)
            # Convert ObjectId to string
            for doc in results:
                if '_id' in doc and hasattr(doc['_id'], '__str__'):
                    doc['_id'] = str(doc['_id'])
            return {
                "operation": "aggregate",
                "count": len(results),
                "results": results
            }
    
    def group(self, key, condition: Dict, initial: Dict, reduce: str) -> Dict:
        """Deprecated: Group documents"""
        with tracer.start_as_current_span("collection.group"):
            results = self.collection.group(key, condition, initial, reduce)
            return {
                "operation": "group",
                "results": results
            }
    
    def map_reduce(self, map_func: str, reduce_func: str, out: str) -> Dict:
        """Execute a map-reduce operation"""
        with tracer.start_as_current_span("collection.map_reduce"):
            result = self.collection.map_reduce(map_func, reduce_func, out)
            return {
                "operation": "map_reduce",
                "collection": result.full_name
            }
    
    def inline_map_reduce(self, map_func: str, reduce_func: str) -> Dict:
        """Execute an inline map-reduce operation"""
        with tracer.start_as_current_span("collection.inline_map_reduce"):
            result = self.collection.inline_map_reduce(map_func, reduce_func)
            return {
                "operation": "inline_map_reduce",
                "results": list(result)
            }
    
    # ========== INDEX OPERATIONS ==========
    
    def create_index(self, keys, **kwargs) -> Dict:
        """Create an index"""
        with tracer.start_as_current_span("collection.create_index"):
            index_name = self.collection.create_index(keys, **kwargs)
            return {
                "operation": "create_index",
                "index_name": index_name
            }
    
    def create_indexes(self, indexes: List) -> Dict:
        """Create multiple indexes"""
        with tracer.start_as_current_span("collection.create_indexes"):
            names = self.collection.create_indexes(indexes)
            return {
                "operation": "create_indexes",
                "index_names": names
            }
    
    def ensure_index(self, key_or_list, **kwargs) -> Dict:
        """Deprecated: Ensure an index exists"""
        with tracer.start_as_current_span("collection.ensure_index"):
            index_name = self.collection.ensure_index(key_or_list, **kwargs)
            return {
                "operation": "ensure_index",
                "index_name": index_name
            }
    
    def drop_index(self, index_or_name) -> Dict:
        """Drop an index"""
        with tracer.start_as_current_span("collection.drop_index"):
            self.collection.drop_index(index_or_name)
            return {
                "operation": "drop_index",
                "dropped": index_or_name
            }
    
    def drop_indexes(self) -> Dict:
        """Drop all indexes except _id"""
        with tracer.start_as_current_span("collection.drop_indexes"):
            self.collection.drop_indexes()
            return {
                "operation": "drop_indexes",
                "status": "all indexes dropped"
            }
    
    def reindex(self) -> Dict:
        """Reindex the collection"""
        with tracer.start_as_current_span("collection.reindex"):
            result = self.collection.reindex()
            return {
                "operation": "reindex",
                "result": result
            }
    
    # ========== COLLECTION OPERATIONS ==========
    
    def distinct(self, key: str, filter_query: Dict = None) -> Dict:
        """Get distinct values for a key"""
        with tracer.start_as_current_span("collection.distinct"):
            filter_query = filter_query or {}
            values = self.collection.distinct(key, filter_query)
            return {
                "operation": "distinct",
                "key": key,
                "values": values,
                "count": len(values)
            }
    
    def rename(self, new_name: str) -> Dict:
        """Rename the collection"""
        with tracer.start_as_current_span("collection.rename"):
            self.collection.rename(new_name)
            self.collection = self.db[new_name]
            return {
                "operation": "rename",
                "new_name": new_name
            }
    
    def drop(self) -> Dict:
        """Drop the collection"""
        with tracer.start_as_current_span("collection.drop"):
            self.collection.drop()
            return {
                "operation": "drop",
                "status": "collection dropped"
            }
    
    # ========== BULK OPERATIONS ==========
    
    def bulk_write(self, requests: List) -> Dict:
        """Execute bulk write operations"""
        with tracer.start_as_current_span("collection.bulk_write"):
            result = self.collection.bulk_write(requests)
            return {
                "operation": "bulk_write",
                "inserted_count": result.inserted_count,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "deleted_count": result.deleted_count,
                "upserted_count": result.upserted_count,
                "acknowledged": result.acknowledged
            }
    
    # ========== UTILITY METHODS ==========
    
    def get_collection_stats(self) -> Dict:
        """Get collection statistics"""
        stats = self.db.command("collStats", self.collection.name)
        return {
            "collection": self.collection.name,
            "count": stats.get('count', 0),
            "size": stats.get('size', 0),
            "indexes": stats.get('nindexes', 0)
        }
    
    def clear_collection(self) -> Dict:
        """Clear all documents from collection"""
        result = self.collection.delete_many({})
        return {
            "operation": "clear_collection",
            "deleted_count": result.deleted_count
        }

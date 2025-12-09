"""
Comprehensive tests for all 35 PyMongo Collection methods
"""
import pytest
from pymongo import IndexModel, ASCENDING, DESCENDING
from pymongo import InsertOne, DeleteOne, UpdateOne, ReplaceOne


class TestInsertOperations:
    """Test insert operations"""
    
    def test_insert_one(self, test_collection):
        document = {"name": "Alice", "age": 30}
        result = test_collection.insert_one(document)
        assert result.acknowledged
        assert result.inserted_id is not None
        
    def test_insert_many(self, test_collection):
        documents = [{"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
        result = test_collection.insert_many(documents)
        assert result.acknowledged
        assert len(result.inserted_ids) == 2
        
    def test_insert(self, test_collection):
        """Deprecated insert method"""
        document = {"name": "Dave", "age": 40}
        result = test_collection.insert(document)
        assert result is not None
        
    def test_save(self, test_collection):
        """Deprecated save method"""
        document = {"name": "Eve", "age": 28}
        result = test_collection.save(document)
        assert result is not None


class TestFindOperations:
    """Test find operations"""
    
    def test_find(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ])
        results = list(test_collection.find())
        assert len(results) == 2
        
    def test_find_one(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.find_one({"name": "Alice"})
        assert result is not None
        assert result["name"] == "Alice"
        
    def test_find_one_and_delete(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.find_one_and_delete({"name": "Alice"})
        assert result is not None
        assert test_collection.count_documents({}) == 0
        
    def test_find_one_and_replace(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.find_one_and_replace(
            {"name": "Alice"},
            {"name": "Alice", "age": 31}
        )
        assert result is not None
        
    def test_find_one_and_update(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.find_one_and_update(
            {"name": "Alice"},
            {"$set": {"age": 31}}
        )
        assert result is not None
        
    def test_find_and_modify(self, test_collection):
        """Deprecated find_and_modify"""
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.find_and_modify(
            query={"name": "Alice"},
            update={"$set": {"age": 31}}
        )
        assert result is not None


class TestUpdateOperations:
    """Test update operations"""
    
    def test_update_one(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.update_one(
            {"name": "Alice"},
            {"$set": {"age": 31}}
        )
        assert result.modified_count == 1
        
    def test_update_many(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"}
        ])
        result = test_collection.update_many(
            {"status": "active"},
            {"$set": {"status": "inactive"}}
        )
        assert result.modified_count == 2
        
    def test_update(self, test_collection):
        """Deprecated update method"""
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.update(
            {"name": "Alice"},
            {"$set": {"age": 31}}
        )
        assert result['ok'] == 1
        
    def test_replace_one(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.replace_one(
            {"name": "Alice"},
            {"name": "Alice", "age": 31, "city": "NYC"}
        )
        assert result.modified_count == 1


class TestDeleteOperations:
    """Test delete operations"""
    
    def test_delete_one(self, test_collection):
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.delete_one({"name": "Alice"})
        assert result.deleted_count == 1
        
    def test_delete_many(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "inactive"},
            {"name": "Bob", "status": "inactive"}
        ])
        result = test_collection.delete_many({"status": "inactive"})
        assert result.deleted_count == 2
        
    def test_remove(self, test_collection):
        """Deprecated remove method"""
        test_collection.insert_one({"name": "Alice", "age": 30})
        result = test_collection.remove({"name": "Alice"})
        assert result['ok'] == 1


class TestCountOperations:
    """Test count operations"""
    
    def test_count(self, test_collection):
        """Deprecated count method"""
        test_collection.insert_many([{"name": f"User{i}"} for i in range(5)])
        count = test_collection.count()
        assert count == 5
        
    def test_count_documents(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"},
            {"name": "Charlie", "status": "inactive"}
        ])
        count = test_collection.count_documents({"status": "active"})
        assert count == 2
        
    def test_estimated_document_count(self, test_collection):
        test_collection.insert_many([{"name": f"User{i}"} for i in range(10)])
        count = test_collection.estimated_document_count()
        assert count >= 10


class TestAggregationOperations:
    """Test aggregation operations"""
    
    def test_aggregate(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "age": 30, "status": "active"},
            {"name": "Bob", "age": 25, "status": "active"},
            {"name": "Charlie", "age": 35, "status": "inactive"}
        ])
        pipeline = [
            {"$match": {"status": "active"}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        results = list(test_collection.aggregate(pipeline))
        assert len(results) > 0
        
    def test_group(self, test_collection):
        """Deprecated group method"""
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"}
        ])
        results = test_collection.group(
            key={"status": 1},
            condition={},
            initial={"count": 0},
            reduce="function(obj, prev) { prev.count++; }"
        )
        assert len(results) > 0
        
    def test_map_reduce(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"}
        ])
        map_func = "function() { emit(this.status, 1); }"
        reduce_func = "function(key, values) { return Array.sum(values); }"
        result = test_collection.map_reduce(map_func, reduce_func, "mr_results")
        assert result.full_name is not None
        
    def test_inline_map_reduce(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"}
        ])
        map_func = "function() { emit(this.status, 1); }"
        reduce_func = "function(key, values) { return Array.sum(values); }"
        results = list(test_collection.inline_map_reduce(map_func, reduce_func))
        assert len(results) > 0


class TestIndexOperations:
    """Test index operations"""
    
    def test_create_index(self, test_collection):
        index_name = test_collection.create_index([("email", ASCENDING)])
        assert index_name is not None
        
    def test_create_indexes(self, test_collection):
        indexes = [
            IndexModel([("name", ASCENDING)]),
            IndexModel([("email", ASCENDING)], unique=True)
        ]
        names = test_collection.create_indexes(indexes)
        assert len(names) == 2
        
    def test_ensure_index(self, test_collection):
        """Deprecated ensure_index"""
        index_name = test_collection.ensure_index([("name", ASCENDING)])
        assert index_name is not None
        
    def test_drop_index(self, test_collection):
        index_name = test_collection.create_index([("temp", ASCENDING)])
        test_collection.drop_index(index_name)
        # Verify index was dropped
        indexes = list(test_collection.list_indexes())
        assert not any(idx['name'] == index_name for idx in indexes)
        
    def test_drop_indexes(self, test_collection):
        test_collection.create_index([("field1", ASCENDING)])
        test_collection.create_index([("field2", ASCENDING)])
        test_collection.drop_indexes()
        # Only _id index should remain
        indexes = list(test_collection.list_indexes())
        assert len(indexes) == 1
        
    def test_reindex(self, test_collection):
        test_collection.insert_many([{"name": f"User{i}"} for i in range(10)])
        result = test_collection.reindex()
        assert result['ok'] == 1


class TestCollectionOperations:
    """Test collection operations"""
    
    def test_distinct(self, test_collection):
        test_collection.insert_many([
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "active"},
            {"name": "Charlie", "status": "inactive"}
        ])
        values = test_collection.distinct("status")
        assert len(values) == 2
        assert "active" in values
        
    def test_rename(self, test_collection, mongo_client, db_name):
        test_collection.insert_one({"name": "Test"})
        new_name = "test_collection_renamed"
        test_collection.rename(new_name)
        # Rename back for cleanup
        db = mongo_client[db_name]
        db[new_name].rename("test_collection")
        
    def test_drop(self, test_collection, mongo_client, db_name):
        test_collection.insert_one({"name": "Test"})
        test_collection.drop()
        # Recreate for other tests
        db = mongo_client[db_name]
        collection = db['test_collection']
        assert collection.count_documents({}) == 0


class TestBulkOperations:
    """Test bulk operations"""
    
    def test_bulk_write(self, test_collection):
        requests = [
            InsertOne({"name": "Alice", "age": 30}),
            InsertOne({"name": "Bob", "age": 25}),
            UpdateOne({"name": "Alice"}, {"$set": {"age": 31}}),
            DeleteOne({"name": "Bob"})
        ]
        result = test_collection.bulk_write(requests)
        assert result.inserted_count == 2
        assert result.modified_count == 1
        assert result.deleted_count == 1

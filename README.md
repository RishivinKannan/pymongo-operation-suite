# PyMongo Testing with Observability

A comprehensive testing framework for PyMongo with integrated observability using OpenTelemetry, Datadog, and Atatus. Test all 35 MongoDB Collection methods through a beautiful web UI.

## 🌟 Features

- **35 MongoDB Operations**: Complete coverage of all PyMongo Collection methods
- **Web UI**: Interactive React dashboard to execute operations
- **Triple Observability**: 
  - OpenTelemetry with Jaeger for distributed tracing
  - Datadog APM integration (optional)
  - Atatus monitoring (optional)
- **Automated Tests**: Comprehensive pytest test suite
- **Docker Compose**: Easy setup with MongoDB replica set

## 📋 Requirements

- Docker & Docker Compose
- Python 3.8+
- Node.js 18+ (for frontend)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd pymongo-test

# Copy environment file
cp .env.example .env

# (Optional) Add your Datadog API key and Atatus license key to .env
```

### 2. Start Infrastructure

```bash
# Start MongoDB and Jaeger
docker-compose up -d

# Wait for MongoDB replica set to initialize (about 30 seconds)
sleep 30
```

### 3. Start Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Flask API
cd backend
python app.py
```

Backend will be available at `http://localhost:5000`

### 4. Start Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 🎯 Using the Application

### Web UI

1. Open `http://localhost:5173` in your browser
2. You'll see all 35 MongoDB operations organized by category:
   - **Insert** (4 methods): insert_one, insert_many, insert, save
   - **Find** (6 methods): find, find_one, find_one_and_delete, find_one_and_replace, find_one_and_update, find_and_modify
   - **Update** (4 methods): update_one, update_many, update, replace_one
   - **Delete** (3 methods): delete_one, delete_many, remove
   - **Count** (3 methods): count, count_documents, estimated_document_count
   - **Aggregation** (4 methods): aggregate, group, map_reduce, inline_map_reduce
   - **Index** (6 methods): create_index, create_indexes, ensure_index, drop_index, drop_indexes, reindex
   - **Collection** (3 methods): distinct, rename, drop
   - **Bulk** (1 method): bulk_write

3. Click on any operation to open the execution form
4. Fill in the parameters (pre-filled with examples)
5. Click "Execute Operation"
6. View results in the dashboard

### Viewing Traces

Access Jaeger UI at `http://localhost:16686` to view distributed traces:
- Service name: `pymongo-testing`
- Each operation creates trace spans
- Inspect timing, errors, and call hierarchy

## 🧪 Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest -v tests/

# Run specific test class
pytest -v tests/test_all_methods.py::TestInsertOperations

# Run with coverage
pytest --cov=backend tests/
```

## 📚 API Endpoints

All operations are available at `http://localhost:5000/api/<operation_name>`:

- `POST /api/insert_one` - Insert a single document
- `POST /api/find` - Find documents
- `POST /api/update_one` - Update a document
- `POST /api/delete_one` - Delete a document
- `POST /api/aggregate` - Run aggregation pipeline
- `POST /api/create_index` - Create an index
- ... (30 more endpoints)

`GET /api/operations` - List all available operations

## 🔧 Configuration

Edit `.env` file:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/?replicaSet=rs0
MONGODB_DB_NAME=testdb

# OpenTelemetry
OTEL_SERVICE_NAME=pymongo-testing
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Datadog (Optional)
DD_API_KEY=your_key_here
DD_SERVICE=pymongo-testing

# Atatus (Optional)
ATATUS_LICENSE_KEY=your_key_here
ATATUS_APP_NAME=pymongo-testing
```

## 📊 Observability Platforms

### OpenTelemetry + Jaeger (Built-in)
- Always enabled
- Jaeger UI: `http://localhost:16686`
- OTLP endpoint: `http://localhost:4317`

### Datadog APM (Optional)
1. Add `DD_API_KEY` to `.env`
2. Configure Datadog agent (or use cloud)
3. View traces in Datadog APM dashboard

### Atatus (Optional)
1. Add `ATATUS_LICENSE_KEY` to `.env`
2. View metrics in Atatus dashboard

## 🛠️ Project Structure

```
pymongo-test/
├── backend/
│   ├── app.py              # Flask API with 35 endpoints
│   ├── database.py         # MongoDB operations
│   └── observability.py    # Observability setup
├── frontend/
│   └── src/
│       ├── App.jsx         # Main app
│       └── components/     # React components
├── tests/
│   └── test_all_methods.py # Comprehensive tests
├── docker-compose.yml      # MongoDB + Jaeger
└── requirements.txt        # Python dependencies
```

## 🐛 Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
docker-compose ps

# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Replica Set Not Initialized
```bash
# Wait longer or manually initialize
docker exec -it pymongo-mongodb mongosh --eval "rs.initiate({_id:'rs0',members:[{_id:0,host:'mongodb:27017'}]})"
```

### Frontend Can't Connect to Backend
- Ensure backend is running on port 5000
- Check CORS settings in `backend/app.py`
- Verify `API_BASE` in `frontend/src/App.jsx`

## 📝 Example Operations

### Insert a Document (UI)
1. Click "insert_one"
2. Modify document: `{"name": "John", "age": 30, "email": "john@example.com"}`
3. Click Execute
4. View trace in Jaeger

### Run Aggregation (API)
```bash
curl -X POST http://localhost:5000/api/aggregate \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline": [
      {"$match": {"age": {"$gte": 25}}},
      {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
  }'
```

## 🤝 Contributing

Contributions welcome! Please test all operations before submitting PRs.

## 📄 License

MIT License - feel free to use for testing and learning!

---

**Made with ❤️ for PyMongo testing and observability**

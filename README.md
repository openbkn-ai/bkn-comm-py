# OpenBKN Common SDK for Python

## Features

- **Multi-Database Support**: MySQL, KingBase, DM (Dameng) databases
- **RDS Driver**: Unified database access interface with Python Database API Specification v2.0

## Installation

```bash
# Install the package
python3 setup.py install
```

## Quick Start

### Using Environment Variables (Recommended)

```python
import os
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

# Set database credentials via environment variables
os.environ['DB_HOST'] = 'your-hostname'
os.environ['DB_PORT'] = '3306'
os.environ['DB_USER'] = 'your-username'
os.environ['DB_PASSWORD'] = 'your-password'
os.environ['DB_NAME'] = 'your-database'

# Create connection pool
w = PooledDBInfo(
    creator=rdsdriver,
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    autocommit=True,
)

# Use the connection
op = PooledDB(master=w, backup=w)
op.execute("CREATE TABLE IF NOT EXISTS users (id INT, name VARCHAR(50))")
```

### Using Configuration File

Create a `config.py` file:

```python
# config.py
DATABASE_CONFIG = {
    'host': 'your-hostname',
    'port': 3306,
    'user': 'your-username',
    'password': 'your-password',
    'database': 'your-database',
    'autocommit': True,
}
```

Use in your code:

```python
from dbutilsx.pooled_db import PooledDB, PooledDBInfo
from config import DATABASE_CONFIG

w = PooledDBInfo(
    creator=rdsdriver,
    **DATABASE_CONFIG
)

op = PooledDB(master=w, backup=w)
```

## Database Support

### MySQL
```python
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

w = PooledDBInfo(
    creator=rdsdriver,
    host='your-mysql-host',
    port=3306,
    user='your-username',
    password='your-password',
    database='your-database',
    autocommit=True,
)
```

### KingBase
```python
import rdsdriver
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

os.environ['DB_TYPE'] = 'KDB9'

w = PooledDBInfo(
    creator=rdsdriver,
    host='your-kingbase-host',
    port=54321,
    user='your-username',
    password='your-password',
    database='your-database',
    autocommit=True,
)
```

### DM (Dameng)
```python
import rdsdriver
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

os.environ['DB_TYPE'] = 'DM8'

w = PooledDBInfo(
    creator=rdsdriver,
    host='your-dm-host',
    port=5236,
    user='your-username',
    password='your-password',
    database='your-database',
    cursorclass=rdsdriver.DictCursor,
)
```

## Connection Types

### PooledDB (Connection Pooling)
Best for applications with frequently changing threads:

```python
from dbutilsx.pooled_db import PooledDB, PooledDBInfo

pool = PooledDB(
    master=w,  # Primary database
    backup=r,  # Backup database (optional)
    mincached=1,      # Minimum cached connections
    maxcached=5,      # Maximum cached connections
    maxconnections=20, # Maximum total connections
    blocking=False,   # Block when no connections available
)
```

### PersistentDB (Persistent Connections)
Best for applications with constant number of threads:

```python
from dbutilsx.persistent_db import PersistentDB, PersistentDBInfo

db = PersistentDB(
    master=w,  # Primary database
    backup=r,  # Backup database (optional)
    maxusage=None,    # Maximum usage count per connection
    ping=1,          # Ping database before using connection
)
```

## Usage Examples

### Basic Operations

```python
# Execute single statement
op.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name VARCHAR(50))")

# Execute with parameters
op.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (1, "John"))

# Execute many
op.executemany("INSERT INTO users (id, name) VALUES (%s, %s)", 
                [(2, "Jane"), (3, "Bob")])

# Query and fetch
results = op.queryAndFetchAll("SELECT * FROM users")
print(results)

# Fetch with size limit
results = op.queryAndFetchMany("SELECT * FROM users", size=2)
print(results)
```

### Using Connection Context Managers

```python
# DB API 2.0 Connection Object
with op.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (1,))
        result = cur.fetchone()
        print(result)
        
        cur.execute("UPDATE users SET name = %s WHERE id = %s", ("John Doe", 1))
        print(f"Updated {cur.rowcount} rows")
```

## Best Practices

### 1. Security
- **Never hardcode credentials** in your source code
- Use environment variables or secure configuration management
- Implement proper access controls and encryption
- Regularly rotate database passwords

### 2. Connection Management
- Always close connections when done
- Use connection pooling for better performance
- Set appropriate connection timeouts
- Monitor connection pool usage

### 3. Error Handling
```python
try:
    op.execute("SELECT * FROM non_existent_table")
except Exception as e:
    print(f"Database error: {e}")
finally:
    # Cleanup if needed
    pass
```

## Environment Variables

Recommended environment variable names:
```bash
# Database Configuration
DB_HOST=your-hostname
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database

# Optional Settings
DB_TYPE=MYSQL  # MYSQL, POSTGRESQL, KINGBASE, DM
DB_CHARSET=utf8mb4
DB_TIMEOUT=30
```

## Documentation

For detailed module documentation, use Python's help system:

```python
import dbutilsx.pooled_db
help(dbutilsx.pooled_db)

import dbutilsx.persistent_db
help(dbutilsx.persistent_db)
```

## Examples

More comprehensive examples are available in the `example/` directory:
- `example/driver.py` - Basic database connection examples
- `example/persistent_db.py` - PersistentDB usage
- `example/pooled_db.py` - Connection pooling examples
- `example/kdb/` - KingBase database examples

## License

This project extends the DBUtils library and follows similar licensing terms.
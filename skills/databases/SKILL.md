---
name: databases
description: Work with MongoDB (document database, BSON documents, aggregation pipelines, Atlas cloud) and PostgreSQL (relational database, SQL queries, psql CLI, pgAdmin). Use when designing schemas, writing queries, optimizing indexes, performing migrations, or administering production databases.
license: MIT
---

# Databases Skill

Unified guide for MongoDB (document-oriented) and PostgreSQL (relational) databases.

## Database Selection Guide

### Choose MongoDB When:
- Frequent schema changes, heterogeneous data
- Natural JSON/BSON data model
- Need horizontal scaling (sharding)
- High write throughput (IoT, logging)
- Rapid prototyping

**Best for:** Content management, catalogs, IoT, real-time analytics, mobile apps

### Choose PostgreSQL When:
- Strong consistency, ACID transactions critical
- Complex relationships, referential integrity
- SQL requirement, BI tools
- Strict schema validation
- Complex queries (window functions, CTEs)

**Best for:** Financial systems, e-commerce, ERP, data warehousing

## Quick Start

### MongoDB
```bash
mongosh "mongodb+srv://cluster.mongodb.net/mydb"

# Basic operations
db.users.insertOne({ name: "Alice", age: 30 })
db.users.find({ age: { $gte: 18 } })
db.users.updateOne({ name: "Alice" }, { $set: { age: 31 } })
```

### PostgreSQL
```bash
psql -U postgres -d mydb

-- Basic operations
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, age INT);
INSERT INTO users (name, age) VALUES ('Alice', 30);
SELECT * FROM users WHERE age >= 18;
```

## Common Operations

### Indexing
```javascript
// MongoDB
db.users.createIndex({ email: 1 })
```

```sql
-- PostgreSQL
CREATE INDEX idx_users_email ON users(email);
```

## Key Differences

| Feature | MongoDB | PostgreSQL |
|---------|---------|------------|
| Data Model | Document (JSON/BSON) | Relational (Tables) |
| Schema | Flexible, dynamic | Strict, predefined |
| Query Language | MongoDB Query Language | SQL |
| Joins | $lookup (limited) | Native, optimized |
| Transactions | Multi-document (4.0+) | Native ACID |
| Scaling | Horizontal (sharding) | Vertical (primary) |

## Best Practices

**MongoDB:**
- Embed documents for 1-to-few relationships
- Reference for 1-to-many or many-to-many
- Index frequently queried fields
- Use aggregation pipeline for complex transformations

**PostgreSQL:**
- Normalize to 3NF, denormalize for performance
- Use foreign keys for referential integrity
- Use EXPLAIN ANALYZE to optimize queries
- Regular VACUUM and ANALYZE maintenance

## Resources

- MongoDB: https://www.mongodb.com/docs/
- PostgreSQL: https://www.postgresql.org/docs/

## Credits

Source: https://github.com/mrgoonie/claudekit-skills

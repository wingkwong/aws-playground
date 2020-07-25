# Database

## Solution Considerations

- Read and write needs
- Total storage requirements
- Typical object size and nature of access to those objects 
- Durability requirements 
- Latency requirements
- Maximum concurrent users to support
- Nature of queries
- Required strength of integrity controls

## NoSQL

- Does your application need transaction support, ACID compliance, joins, or SQL
- Can your application do without these for all, some, or part of its data models?
    - Refactor database hotspots to NoSQL solutions
- Can offer increases in flexibility, availability, scalability and performance

### NoSQL on Amazon EC2

Cassandra, HBase, Redis, MongoDB, Couchbase, and Riak

### Managed NoSQL

Amazon DynamoDB, Amazon Neptune, EastiCache with Redis and Amazon EMR supports HBase

### Use cases

- Leaderboards and scoring
- Rapid ingestion of clickstream or log data
- Temporary data needs (cart data)
- Hot tables
- Metadata or lookup tables
- Session data


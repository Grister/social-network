# social-network

### Installation

Clone the repository
```
git clone https://github.com/akushyn/social-network.git
```

Install project dependencies
```
cd social-network
pip3 install -r requirements.txt
```

Copy `env.example` to `.env` with initial configurations
```
cp env.example .env
```

### Setup database

Install Postgres from official site.

When you have done with installing PostgreSQL on your pc, follow next steps to: 

- create database
- create database user

```
sudo su - postgres
psql
CREATE DATABASE network;
CREATE USER network WITH PASSWORD 'network';
ALTER USER network WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE network TO network;
```

### Flask-Migrate

Initialize migrations
```
flask db init
```

Create db migration: 
```
flask db migrate
``` 
or
```
flask db migrate -m 'add short message'
```

Upgrade database to head revision
```
flask db upgrade
```

Downgrade database revision
```
flask db downgrade
```

### CLI commands

Generate `n` fake users
```
cd social-network
flask fake users 5
```
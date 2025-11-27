# ServiceID

Microservices-based authentication and authorization system built on FastAPI with JWT token support (RSA256).

## 🏗️ Architecture

The project consists of the following components:

- **API Service** (`services/api`) - Main FastAPI service
- **Shared Core** (`shared/core`) - Shared modules for all services
  - Configuration
  - JWT tokens
  - RSA keys
  - Logging

## 🚀 Quick Start

### Requirements

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone <repository-url>
cd serviceID
```

2. Create a `.env` file (optional, default values will be used):
```bash
cp .env.example .env  # if .env.example exists
```

3. Start all services:
```bash
docker-compose up -d --build
```

4. Check status:
```bash
docker-compose ps
```

5. Check API logs:
```bash
docker-compose logs -f api
```

## 📋 Services

### API Service (Gateway API)

- **Port**: 8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **JWKS Endpoint**: http://localhost:8000/.well-known/jwks.json

### PostgreSQL

- **Port**: 5433 (localhost) → 5432 (container)
- **Database**: `main` (default)
- **User**: `user` (default)
- **Password**: `pass123` (default)

### Redis

- **Port**: 6380 (localhost) → 6379 (container)

## 🔧 Configuration

Configuration is managed through environment variables. You can use a `.env` file or pass variables directly in `docker-compose.yaml`.

### Project Structure

```
serviceID/
├── docker-compose.yaml       # Docker Compose configuration
├── services/
│   └── api/                  # API service
│       ├── app/
│       │   ├── core/         # Core configuration
│       │   ├── models/       # SQLAlchemy models
│       │   ├── routes/       # API routes
│       │   ├── schemas/      # Pydantic schemas
│       │   └── security/     # Security (password hashing)
│       ├── Dockerfile
│       └── requirements.txt
└── shared/
    └── core/                 # Shared modules
        ├── config.py         # Base settings
        ├── jwt_tokens.py     # JWT handling
        ├── rsa_keys.py       # RSA key generation
        └── logging.py        # Logging configuration
```

## 🔒 Security

- Passwords are hashed using `passlib` (bcrypt)
- JWT tokens are signed with RSA256 keys
- RSA keys are automatically generated on first startup
- Public keys are available via JWKS endpoint

## 📦 Dependencies

Main dependencies:
- FastAPI - Web framework
- SQLAlchemy - ORM
- Pydantic - Data validation
- PyJWT - JWT token handling
- Passlib - Password hashing
- psycopg2-binary - PostgreSQL driver

See `services/api/requirements.txt` for the full list of dependencies.

## 📝 License

See [LICENSE](LICENSE) file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues, please create an issue in the repository.

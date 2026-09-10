# Double Entry Ledger System

A backend-focused **double-entry accounting and payment ledger system** built with **FastAPI, SQLAlchemy, PostgreSQL, Redis, and Docker**.

The project is designed around financial correctness, transaction integrity, idempotency, concurrency control, and production-oriented backend engineering practices.

---

## 🚀 Features

### Authentication & Authorization

- User registration and login
- JWT-based authentication
- Protected payment endpoints
- Current-user identification through JWT
- Password hashing

### Account Management

- User accounts
- Account status management
- Account types
- Account currency
- Opening account balance
- User-to-account relationship

### Double-Entry Ledger

Every financial transaction creates corresponding ledger entries.

For a transfer:

```text
Sender Account
    Credit → amount

Receiver Account
    Debit → amount


## How to Run the Project

There are two ways to run the project:

1. Local Development — FastAPI runs locally, PostgreSQL and Redis run in Docker.
2. Docker Compose — FastAPI, PostgreSQL, Redis, and pgAdmin all run in Docker.

---

## Prerequisites

Make sure you have installed:

- Python 3.13+
- Docker
- Docker Compose
- Git

Check the installations:

```bash
python3.13 --version
docker --version
docker compose version
git --version
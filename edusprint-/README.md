# EduSprint Project Manager

A comprehensive management script for the EduSprint Django project that simplifies common development tasks.

## Features

The manager provides the following commands:

- **install** - Install project dependencies
- **setup** - Setup database and run migrations
- **run** - Start development server
- **test** - Run project tests
- **static** - Collect static files
- **backup** - Create database backup
- **health** - Check project health
- **clean** - Clean temporary files and caches
- **superuser** - Create a superuser

## Usage

### Basic Commands

```bash
# Show help
python manager.py

# Install dependencies
python manager.py install

# Setup database and run migrations
python manager.py setup

# Start development server
python manager.py run

# Run tests
python manager.py test

# Check project health
python manager.py health
```

### Advanced Commands

```bash
# Start server on specific host and port
python manager.py run --host 0.0.0.0 --port 8000

# Create database backup
python manager.py backup

# Collect static files
python manager.py static

# Clean project cache
python manager.py clean

# Create superuser
python manager.py superuser
```

## Project Structure

```
edusprint-/
├── manager.py              # Project manager script
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
├── edusprint/             # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                 # Custom user app
│   ├── models.py
│   ├── views.py
│   └── serializers.py
└── portfolio/             # Portfolio app
    ├── models.py
    ├── views.py
    └── serializers.py
```

## Database Configuration

The project uses MySQL database with the following configuration:
- Database: `edusprint_db`
- User: `root`
- Password: `12341234`
- Host: `localhost`
- Port: `3306`

## Quick Start

1. **Install dependencies:**
   ```bash
   python manager.py install
   ```

2. **Setup database:**
   ```bash
   python manager.py setup
   ```

3. **Start development server:**
   ```bash
   python manager.py run
   ```

4. **Check project health:**
   ```bash
   python manager.py health
   ```

## Development Workflow

1. **Daily development:**
   ```bash
   python manager.py run
   ```

2. **After making model changes:**
   ```bash
   python manager.py setup
   ```

3. **Before committing:**
   ```bash
   python manager.py test
   python manager.py health
   ```

4. **Clean up:**
   ```bash
   python manager.py clean
   ```

## Troubleshooting

### Common Issues

1. **Database connection error:**
   - Ensure MySQL server is running
   - Check database credentials in `edusprint/settings.py`

2. **Import errors:**
   - Run `python manager.py install` to install dependencies
   - Activate virtual environment if using one

3. **Migration errors:**
   - Run `python manager.py setup` to reset migrations
   - Check for conflicting model changes

### Health Check

Use the health check command to diagnose issues:

```bash
python manager.py health
```

This will check:
- Database connectivity
- Django app configuration
- Static files directory
- Media files directory

## Contributing

When adding new features:

1. Update `requirements.txt` if adding new dependencies
2. Test with `python manager.py test`
3. Check health with `python manager.py health`
4. Update this README if adding new commands 
# Edusprint

"""
EduSprint Project Manager
A comprehensive management script for the EduSprint Django project.
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edusprint.settings')

# Initialize Django only when needed
def setup_django():
    """Setup Django environment"""
    try:
        import django
        django.setup()
        return True
    except ImportError as e:
        print(f"❌ Django not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error setting up Django: {e}")
        return False

def execute_django_command(command):
    """Execute Django management commands"""
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line([sys.argv[0], command])
    except Exception as e:
        print(f"Error running Django command '{command}': {e}")

class EduSprintManager:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.project_name = "edusprint"
        
    def run_django_command(self, command):
        """Run Django management commands"""
        execute_django_command(command)
            
    def install_dependencies(self):
        """Install project dependencies"""
        print("Installing project dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed successfully!")
        except FileNotFoundError:
            print("❌ requirements.txt not found. Creating one...")
            self.create_requirements()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            
    def create_requirements(self):
        """Create requirements.txt file"""
        requirements = [
            "Django>=5.2.3",
            "djangorestframework",
            "djangorestframework-simplejwt",
            "mysqlclient",
            "Pillow",
            "python-decouple",
            "django-cors-headers",
        ]
        
        with open("requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        print("✅ requirements.txt created!")
        
    def setup_database(self):
        """Setup and migrate database"""
        if not setup_django():
            return
            
        print("Setting up database...")
        try:
            # Run migrations
            self.run_django_command("makemigrations")
            self.run_django_command("migrate")
            
            # Create superuser if needed
            print("Do you want to create a superuser? (y/n): ", end="")
            if input().lower() == 'y':
                self.run_django_command("createsuperuser")
                
            print("✅ Database setup completed!")
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            
    def run_server(self, host="127.0.0.1", port="8000"):
        """Run development server"""
        print(f"Starting development server on {host}:{port}...")
        try:
            subprocess.run([
                sys.executable, "manage.py", "runserver", f"{host}:{port}"
            ], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            
    def run_tests(self):
        """Run project tests"""
        print("Running tests...")
        try:
            subprocess.run([sys.executable, "manage.py", "test"], check=True)
            print("✅ Tests completed!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
        except FileNotFoundError:
            print("❌ manage.py not found in current directory")
            
    def collect_static(self):
        """Collect static files"""
        print("Collecting static files...")
        try:
            subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
            print("✅ Static files collected!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error collecting static files: {e}")
        except FileNotFoundError:
            print("❌ manage.py not found in current directory")
            
    def backup_database(self):
        """Create database backup"""
        if not setup_django():
            return
            
        print("Creating database backup...")
        try:
            from django.conf import settings
            db_settings = settings.DATABASES['default']
            
            backup_dir = self.base_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            # Use Python datetime instead of shell date command
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"backup_{self.project_name}_{timestamp}.sql"
            
            # MySQL backup command
            cmd = [
                "mysqldump",
                "-u", db_settings['USER'],
                f"-p{db_settings['PASSWORD']}",
                "-h", db_settings['HOST'],
                "-P", str(db_settings['PORT']),
                db_settings['NAME']
            ]
            
            with open(backup_file, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
                
            print(f"✅ Database backup created: {backup_file}")
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            
    def check_health(self):
        """Check project health"""
        if not setup_django():
            return
            
        print("Checking project health...")
        
        # Check if database is accessible
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✅ Database connection: OK")
        except Exception as e:
            print(f"❌ Database connection: FAILED - {e}")
            
        # Check if all apps are properly configured
        try:
            from django.apps import apps
            apps.check_apps_ready()
            print("✅ Django apps: OK")
        except Exception as e:
            print(f"❌ Django apps: FAILED - {e}")
            
        # Check and create static files directory
        static_dir = self.base_dir / "static"
        if static_dir.exists():
            print("✅ Static files directory: OK")
        else:
            static_dir.mkdir(exist_ok=True)
            print("✅ Static files directory: Created")
            
        # Check and create media files directory
        media_dir = self.base_dir / "media"
        if media_dir.exists():
            print("✅ Media files directory: OK")
        else:
            media_dir.mkdir(exist_ok=True)
            print("✅ Media files directory: Created")
            
    def clean_project(self):
        """Clean temporary files and caches"""
        print("Cleaning project...")
        
        # Remove Python cache files
        for root, dirs, files in os.walk(self.base_dir):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    cache_dir = Path(root) / dir_name
                    shutil.rmtree(cache_dir)
                    print(f"🗑️  Removed: {cache_dir}")
                    
        # Remove .pyc files
        for pyc_file in self.base_dir.rglob("*.pyc"):
            pyc_file.unlink()
            print(f"🗑️  Removed: {pyc_file}")
            
        print("✅ Project cleaned!")
        
    def create_superuser(self):
        """Create a superuser"""
        print("Creating superuser...")
        try:
            subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)
            print("✅ Superuser created!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating superuser: {e}")
        except FileNotFoundError:
            print("❌ manage.py not found in current directory")
            
    def show_help(self):
        """Show help information"""
        help_text = """
EduSprint Project Manager

Available commands:
  install          Install project dependencies
  setup            Setup database and run migrations
  run              Start development server
  test             Run project tests
  static           Collect static files
  backup           Create database backup
  health           Check project health
  clean            Clean temporary files and caches
  superuser        Create a superuser
  help             Show this help message

Examples:
  python manager.py install
  python manager.py setup
  python manager.py run
  python manager.py run --host 0.0.0.0 --port 8000
  python manager.py test
  python manager.py health
        """
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description="EduSprint Project Manager")
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("--host", default="127.0.0.1", help="Host for development server")
    parser.add_argument("--port", default="8000", help="Port for development server")
    
    args = parser.parse_args()
    
    manager = EduSprintManager()
    
    if not args.command:
        manager.show_help()
        return
        
    command = args.command.lower()
    
    if command == "install":
        manager.install_dependencies()
    elif command == "setup":
        manager.setup_database()
    elif command == "run":
        manager.run_server(args.host, args.port)
    elif command == "test":
        manager.run_tests()
    elif command == "static":
        manager.collect_static()
    elif command == "backup":
        manager.backup_database()
    elif command == "health":
        manager.check_health()
    elif command == "clean":
        manager.clean_project()
    elif command == "superuser":
        manager.create_superuser()
    elif command == "help":
        manager.show_help()
    else:
        print(f"❌ Unknown command: {command}")
        manager.show_help()

if __name__ == "__main__":
    main() 
"""
Verify all required packages are installed correctly
Run this after pip install to check for issues
"""

import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report status"""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✅ {package_name}: OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: FAILED - {e}")
        return False

def main():
    print("="*60)
    print("PACKAGE VERIFICATION")
    print("="*60)
    print()
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    print()
    
    # Critical packages
    print("Checking critical packages...")
    critical = [
        ("pkg_resources", "setuptools"),
        ("fastapi", "fastapi"),
        ("sqlalchemy", "sqlalchemy"),
        ("uvicorn", "uvicorn"),
        ("gunicorn", "gunicorn"),
        ("razorpay", "razorpay"),
        ("pydantic", "pydantic"),
        ("jose", "python-jose"),
        ("passlib", "passlib"),
    ]
    
    critical_ok = all(check_import(mod, pkg) for mod, pkg in critical)
    print()
    
    # Optional packages
    print("Checking optional packages...")
    optional = [
        ("twilio.rest", "twilio"),
        ("sendgrid", "sendgrid"),
        ("google.generativeai", "google-generativeai"),
        ("PIL", "Pillow"),
    ]
    
    optional_ok = all(check_import(mod, pkg) for mod, pkg in optional)
    print()
    
    # Database adapters
    print("Checking database adapters...")
    db = [
        ("psycopg2", "psycopg2-binary"),
    ]
    
    db_ok = all(check_import(mod, pkg) for mod, pkg in db)
    print()
    
    # Summary
    print("="*60)
    if critical_ok and db_ok:
        print("✅ ALL CRITICAL PACKAGES INSTALLED SUCCESSFULLY!")
        print("="*60)
        print()
        print("You can now start the server:")
        print("  uvicorn app.main:app --reload")
        return 0
    else:
        print("❌ SOME PACKAGES FAILED TO INSTALL")
        print("="*60)
        print()
        print("Try:")
        print("  pip install --upgrade pip setuptools wheel")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

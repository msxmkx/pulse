#!/usr/bin/env python3
"""
Test script to verify the Flask app can be imported and started correctly.
This helps debug deployment issues on Render.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    try:
        print("Testing imports...")
        import flask
        print("✓ Flask imported successfully")
        
        import yfinance
        print("✓ yfinance imported successfully")
        
        import pandas
        print("✓ pandas imported successfully")
        
        import numpy
        print("✓ numpy imported successfully")
        
        import requests
        print("✓ requests imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_import():
    """Test if the main app can be imported."""
    try:
        print("\nTesting app import...")
        from app_monochrome import app
        print("✓ app_monochrome.py imported successfully")
        print(f"✓ Flask app object: {type(app)}")
        return True
    except Exception as e:
        print(f"✗ App import error: {e}")
        return False

def test_app_start():
    """Test if the app can start without errors."""
    try:
        print("\nTesting app startup...")
        from app_monochrome import app
        
        # Test if the app has the expected routes
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✓ App has {len(routes)} routes")
        print(f"✓ Routes: {routes[:5]}...")  # Show first 5 routes
        
        return True
    except Exception as e:
        print(f"✗ App startup error: {e}")
        return False

if __name__ == "__main__":
    print("=== Deployment Test Script ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Files in directory: {len(os.listdir('.'))}")
    
    success = True
    success &= test_imports()
    success &= test_app_import()
    success &= test_app_start()
    
    if success:
        print("\n🎉 All tests passed! App should deploy successfully.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1) 
#!/usr/bin/env python3
"""
Test script to verify the build process works on Render.
This helps identify what's causing the build failure.
"""

import sys
import os

def test_basic_imports():
    """Test basic imports that should work on Render"""
    try:
        print("Testing basic imports...")
        
        # Test Flask
        import flask
        print("✓ Flask imported successfully")
        
        # Test yfinance
        import yfinance
        print("✓ yfinance imported successfully")
        
        # Test pandas
        import pandas
        print("✓ pandas imported successfully")
        
        # Test numpy
        import numpy
        print("✓ numpy imported successfully")
        
        # Test requests
        import requests
        print("✓ requests imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_import():
    """Test if the main app can be imported"""
    try:
        print("\nTesting app import...")
        import app_monochrome
        print("✓ app_monochrome imported successfully")
        
        # Test if the app object exists
        if hasattr(app_monochrome, 'app'):
            print("✓ Flask app object found")
        else:
            print("✗ Flask app object not found")
            return False
            
        return True
    except Exception as e:
        print(f"✗ App import error: {e}")
        return False

def test_gunicorn():
    """Test if gunicorn can start the app"""
    try:
        print("\nTesting gunicorn compatibility...")
        import gunicorn
        print("✓ gunicorn imported successfully")
        return True
    except ImportError as e:
        print(f"✗ gunicorn import error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Render Build Test")
    print("=" * 30)
    
    success = True
    
    # Test basic imports
    if not test_basic_imports():
        success = False
    
    # Test app import
    if not test_app_import():
        success = False
    
    # Test gunicorn
    if not test_gunicorn():
        success = False
    
    print("\n" + "=" * 30)
    if success:
        print("✅ All tests passed! Build should work on Render.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""Test script to verify FlowManager Python installation"""

import sys
import json


def test_config():
    try:
        with open("cfg.json", "r") as f:
            cfg = json.load(f)
        print("✓ Configuration file loaded successfully")
        print(f"  - Port: {cfg['port']}")
        print(f"  - Projects: {len(cfg['projects'])}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_imports():
    required_modules = ["fastapi", "uvicorn", "cryptography"]
    success = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} imported successfully")
        except ImportError as e:
            print(f"✗ {module} import failed: {e}")
            success = False
    return success


if __name__ == "__main__":
    print("FlowManager Python - Installation Test")
    print("=" * 40)

    tests = [("Configuration", test_config), ("Python Modules", test_imports)]
    all_passed = True
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}:")
        if not test_func():
            all_passed = False

    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! FlowManager is ready to run.")
    else:
        print("✗ Some tests failed. Install dependencies first.")
        sys.exit(1)

import sys
import platform
import importlib
import os

# =================================================================
# Project: FinOps Environment Validator (Fixed)
# Author: Yusri Ajam
# Description: Validates the installation of the Python stack 
#              while ensuring VENV alignment.
# =================================================================

def check_libraries():
    # Updated list to include the "Fuzzy" matching stack
    libraries = {
        "pandas": "pandas",
        "numpy": "numpy",
        "sklearn": "scikit-learn", 
        "flask": "flask",
        "sqlalchemy": "sqlalchemy",
        "requests": "requests",
        "thefuzz": "thefuzz",
        "Levenshtein": "python-Levenshtein"
    }
    
    print(f"--- Environment Validation: {platform.system()} ---")
    print(f"Python Executable: {sys.executable}") # THIS TELLS YOU IF YOU ARE IN VENV
    print(f"Python Version:    {sys.version.split()[0]}\n")
    
    # Check if we are actually in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  WARNING: Running on SYSTEM Python. (VENV not detected)\n")
    else:
        print("✅ SUCCESS: Running inside Virtual Environment.\n")

    all_passed = True
    
    for lib_import, lib_name in libraries.items():
        try:
            # Dynamically import
            module = importlib.import_module(lib_import)
            
            # Use getattr with a fallback for versioning
            version = getattr(module, "__version__", "Found")
            print(f"✅ {lib_import.ljust(15)} : Installed (v{version})")
            
        except ImportError:
            print(f"❌ {lib_import.ljust(15)} : NOT FOUND ({lib_name})")
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("FINAL RESULT: Environment is READY for FinOps.")
    else:
        print("FINAL RESULT: Environment is INCOMPLETE.")
        print("Action: Run './.venv/bin/pip install pandas thefuzz python-Levenshtein'")
    print("="*50)

if __name__ == "__main__":
    check_libraries()
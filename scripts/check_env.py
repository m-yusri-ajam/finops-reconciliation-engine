import sys
import platform
import importlib

# =================================================================
# Project: FinOps Environment Validator
# Author: Yusri Ajam
# Description: Validates the installation of the Python stack 
#              required for Financial Data Automation.
# =================================================================

def check_libraries():
    # List of libraries to verify
    libraries = [
        "pandas", 
        "numpy", 
        "sklearn", 
        "flask", 
        "sqlalchemy", 
        "requests"
    ]
    
    print(f"--- Environment Validation: {platform.system()} ({platform.release()}) ---")
    print(f"Python Version: {sys.version.split()[0]}\n")
    
    all_passed = True
    
    for lib in libraries:
        try:
            # Dynamically import the library
            module = importlib.import_module(lib)
            # Handle scikit-learn's specific version attribute name
            version = getattr(module, "__version__", "Version Hidden")
            print(f"✅ {lib.ljust(12)} : Installed (v{version})")
        except ImportError:
            print(f"❌ {lib.ljust(12)} : NOT FOUND")
            all_passed = False

    print("\n" + "="*40)
    if all_passed:
        print("RESULT: Environment is READY for FinOps Automation.")
    else:
        print("RESULT: Environment is INCOMPLETE. Please re-run setup_env.sh.")
    print("="*40)

if __name__ == "__main__":
    check_libraries()

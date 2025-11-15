#!/usr/bin/env python3
"""
Setup Verification Script for KSL Preprocessing Tool
Checks if the environment is properly configured before running the preprocessing.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print(f"\n{'=' * 80}")
    print(f"  {text}")
    print(f"{'=' * 80}\n")

def print_status(check_name, passed, message=""):
    """Print status of a check."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {check_name}")
    if message:
        print(f"       {message}")

def check_python_version():
    """Check if Python version is 3.6 or higher."""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 6
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if passed:
        print_status("Python Version", True, f"Python {version_str} detected")
    else:
        print_status("Python Version", False, 
                    f"Python {version_str} detected, but Python 3.6+ required")
    
    return passed

def check_dependencies():
    """Check if required packages are installed."""
    results = {}
    
    # Check tqdm
    try:
        import tqdm
        version = tqdm.__version__
        print_status("tqdm package", True, f"Version {version}")
        results['tqdm'] = True
    except ImportError:
        print_status("tqdm package", False, 
                    "Not installed. Run: pip3 install -r requirements.txt")
        results['tqdm'] = False
    
    # Standard library imports (should always be available)
    required_stdlib = ['json', 'os', 'shutil', 'glob', 'logging', 'multiprocessing']
    all_stdlib_ok = True
    
    for module in required_stdlib:
        try:
            __import__(module)
        except ImportError:
            print_status(f"{module} module", False, "Standard library module missing")
            all_stdlib_ok = False
    
    if all_stdlib_ok:
        print_status("Standard library modules", True, "All required modules available")
    
    results['stdlib'] = all_stdlib_ok
    
    return all(results.values())

def check_data_directory():
    """Check if data directory exists."""
    data_root = "/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets"
    word_dir = os.path.join(data_root, "Training", "Labeled", "REAL", "WORD")
    morpheme_dir = os.path.join(word_dir, "morpheme")
    
    results = {}
    
    # Check data root
    if os.path.exists(data_root):
        print_status("Data root directory", True, data_root)
        results['data_root'] = True
    else:
        print_status("Data root directory", False, 
                    f"Not found: {data_root}")
        results['data_root'] = False
    
    # Check WORD directory
    if os.path.exists(word_dir):
        print_status("WORD directory", True, word_dir)
        results['word_dir'] = True
        
        # Count numbered folders
        try:
            numbered_folders = [d for d in os.listdir(word_dir) 
                              if os.path.isdir(os.path.join(word_dir, d)) and d.isdigit()]
            print(f"       Found {len(numbered_folders)} numbered folders: {', '.join(sorted(numbered_folders))}")
        except Exception as e:
            print(f"       Warning: Could not list folders: {e}")
    else:
        print_status("WORD directory", False, f"Not found: {word_dir}")
        results['word_dir'] = False
    
    # Check morpheme directory
    if os.path.exists(morpheme_dir):
        print_status("Morpheme directory", True, morpheme_dir)
        results['morpheme_dir'] = True
    else:
        print_status("Morpheme directory", False, f"Not found: {morpheme_dir}")
        results['morpheme_dir'] = False
    
    return all(results.values())

def check_output_directory():
    """Check if output directory can be created."""
    output_dir = "/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed"
    
    if os.path.exists(output_dir):
        print_status("Output directory", True, f"Already exists: {output_dir}")
        
        # Check if writable
        if os.access(output_dir, os.W_OK):
            print(f"       Directory is writable")
            return True
        else:
            print_status("Output directory writable", False, "Directory is not writable")
            return False
    else:
        # Check if parent directory is writable
        parent_dir = os.path.dirname(output_dir)
        if os.path.exists(parent_dir) and os.access(parent_dir, os.W_OK):
            print_status("Output directory", True, 
                        f"Can be created at: {output_dir}")
            return True
        else:
            print_status("Output directory", False, 
                        f"Cannot create at: {output_dir}")
            return False

def check_disk_space():
    """Check available disk space."""
    try:
        import shutil
        output_parent = "/Users/jaylee_83/Documents/_D-ALabs/Data_Sets"
        
        if os.path.exists(output_parent):
            stat = shutil.disk_usage(output_parent)
            free_gb = stat.free / (1024**3)
            
            # Require at least 50 GB free space
            if free_gb >= 50:
                print_status("Disk space", True, 
                           f"{free_gb:.1f} GB available (≥50 GB recommended)")
                return True
            else:
                print_status("Disk space", False, 
                           f"{free_gb:.1f} GB available (≥50 GB recommended)")
                return False
        else:
            print_status("Disk space", False, "Cannot check - directory not found")
            return False
    except Exception as e:
        print_status("Disk space", False, f"Cannot check: {e}")
        return False

def check_cpu_cores():
    """Check number of CPU cores for multiprocessing."""
    import multiprocessing
    
    cpu_count = multiprocessing.cpu_count()
    recommended_workers = max(1, cpu_count - 1)
    
    print_status("CPU cores", True, 
                f"{cpu_count} cores detected (recommended workers: {recommended_workers})")
    return True

def main():
    """Run all verification checks."""
    print_header("KSL Preprocessing Tool - Setup Verification")
    
    print("이 스크립트는 전처리 도구를 실행하기 전에 환경을 검증합니다.")
    print("This script verifies your environment before running the preprocessing tool.")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Data Directories", check_data_directory),
        ("Output Directory", check_output_directory),
        ("Disk Space", check_disk_space),
        ("CPU Cores", check_cpu_cores),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print_header(check_name)
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_status(check_name, False, f"Error during check: {e}")
            results[check_name] = False
    
    # Summary
    print_header("Summary")
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    print()
    
    if all(results.values()):
        print("🎉 All checks passed! You're ready to run the preprocessing tool.")
        print()
        print("Quick start:")
        print("  ./run_preprocessing.sh")
        print()
        print("Or run directly:")
        print("  python3 trim_sign_language_data.py --dry-run")
        print("  python3 trim_sign_language_data.py --multiprocessing")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above before running.")
        print()
        print("Common solutions:")
        print("  - Install dependencies: pip3 install -r requirements.txt")
        print("  - Check data paths in the script")
        print("  - Ensure sufficient disk space")
        return 1

if __name__ == '__main__':
    sys.exit(main())


#!/usr/bin/env python3
"""
Korean Sign Language (KSL) Data Preprocessing Script
Trims sign language keypoint data by removing 10 frames before action start and 10 frames after action end.
Only processes Front (F) view data.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import glob
import logging
from datetime import datetime
from tqdm import tqdm
import multiprocessing as mp
from functools import partial


# Configure logging
def setup_logging(log_file: str = None):
    """Setup logging configuration."""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)


def load_morpheme_data(morpheme_path: str) -> Tuple[float, float, float]:
    """
    Load morpheme JSON file to get action start and end times.
    
    Args:
        morpheme_path: Path to morpheme JSON file
        
    Returns:
        Tuple of (start_time, end_time, duration)
    """
    with open(morpheme_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    start_time = data['data'][0]['start']
    end_time = data['data'][0]['end']
    duration = data['metaData']['duration']
    
    return start_time, end_time, duration


def get_frame_range(start_time: float, end_time: float, duration: float, 
                    total_frames: int, offset: int = 10) -> Tuple[int, int]:
    """
    Calculate frame range to keep based on action timing.
    
    Args:
        start_time: Action start time in seconds
        end_time: Action end time in seconds
        duration: Total video duration in seconds
        total_frames: Total number of frames
        offset: Number of frames to trim before start and after end
        
    Returns:
        Tuple of (start_frame, end_frame) to keep
    """
    fps = total_frames / duration
    
    start_frame = int(start_time * fps) - offset
    end_frame = int(end_time * fps) + offset
    
    # Ensure frames are within valid range
    start_frame = max(0, start_frame)
    end_frame = min(total_frames - 1, end_frame)
    
    return start_frame, end_frame


def process_sign_folder(keypoint_folder: str, morpheme_folder: str, 
                       output_base: str, dry_run: bool = False) -> Dict:
    """
    Process a single sign language folder (F view only).
    
    Args:
        keypoint_folder: Path to folder containing keypoint JSON files
        morpheme_folder: Path to folder containing morpheme JSON files
        output_base: Base output directory
        dry_run: If True, only report what would be done without copying
        
    Returns:
        Dictionary with processing statistics
    """
    folder_name = os.path.basename(keypoint_folder)
    
    # Only process F (Front) view data
    if '_F' not in folder_name:
        return {'skipped': True, 'reason': 'Not F view'}
    
    # Extract WORD number and view direction from folder name
    # Example: NIA_SL_WORD0001_REAL02_F -> WORD0001, F
    parts = folder_name.split('_')
    word_num = None
    view_dir = None
    
    for part in parts:
        if part.startswith('WORD'):
            word_num = part
        if part in ['F', 'D', 'L', 'R', 'U']:
            view_dir = part
    
    if not word_num or not view_dir:
        return {'error': f"Cannot parse folder name: {folder_name}"}
    
    # Find corresponding morpheme file using flexible pattern
    # Pattern: NIA_SL_WORD0001_REAL*_F_morpheme.json
    morpheme_pattern = os.path.join(morpheme_folder, f"NIA_SL_{word_num}_REAL*_{view_dir}_morpheme.json")
    morpheme_files = glob.glob(morpheme_pattern)
    
    if not morpheme_files:
        return {'error': f"Morpheme file not found with pattern: {morpheme_pattern}"}
    
    # Use the first matching file
    morpheme_file = morpheme_files[0]
    
    # If multiple files found, log a warning but continue with the first one
    if len(morpheme_files) > 1:
        # Just use the first one silently
        pass
    
    # Get all keypoint files
    keypoint_files = sorted(glob.glob(os.path.join(keypoint_folder, "*_keypoints.json")))
    total_frames = len(keypoint_files)
    
    if total_frames == 0:
        return {'error': "No keypoint files found"}
    
    # Load morpheme data
    try:
        start_time, end_time, duration = load_morpheme_data(morpheme_file)
    except Exception as e:
        return {'error': f"Error loading morpheme data: {e}"}
    
    # Calculate frame range
    start_frame, end_frame = get_frame_range(start_time, end_time, duration, total_frames)
    frames_to_keep = end_frame - start_frame + 1
    
    # Create output directory
    output_folder = os.path.join(output_base, folder_name)
    
    if not dry_run:
        os.makedirs(output_folder, exist_ok=True)
    
    # Copy selected frames
    copied_count = 0
    for i, frame_idx in enumerate(range(start_frame, end_frame + 1)):
        src_file = keypoint_files[frame_idx]
        
        if not dry_run:
            # Create new filename with sequential numbering
            base_name = os.path.basename(src_file)
            parts = base_name.split('_')
            # Replace frame number with new sequential number
            parts[-2] = f"{i:012d}"
            new_name = '_'.join(parts)
            
            dst_file = os.path.join(output_folder, new_name)
            shutil.copy2(src_file, dst_file)
        
        copied_count += 1
    
    return {
        'success': True,
        'folder': folder_name,
        'total_frames': total_frames,
        'start_frame': start_frame,
        'end_frame': end_frame,
        'kept_frames': frames_to_keep,
        'trimmed_frames': total_frames - frames_to_keep,
        'start_time': start_time,
        'end_time': end_time
    }


def process_single_folder_wrapper(args):
    """Wrapper function for multiprocessing."""
    keypoint_folder, morpheme_folder, output_folder_base, dry_run = args
    return process_sign_folder(keypoint_folder, morpheme_folder, output_folder_base, dry_run)


def process_dataset(data_root: str, output_base: str, dry_run: bool = False, 
                   error_log_path: str = None, use_multiprocessing: bool = False,
                   num_workers: int = None):
    """
    Process entire dataset.
    
    Args:
        data_root: Root directory of the dataset
        output_base: Output directory for processed data
        dry_run: If True, only report what would be done
        error_log_path: Path to save error log file
        use_multiprocessing: If True, use multiprocessing for parallel processing
        num_workers: Number of worker processes (defaults to CPU count)
    """
    keypoint_base = os.path.join(data_root, "Training", "Labeled", "REAL", "WORD")
    morpheme_base = os.path.join(keypoint_base, "morpheme")
    
    # Find all numbered folders (01, 02, 03, etc.)
    numbered_folders = sorted([d for d in os.listdir(keypoint_base) 
                              if os.path.isdir(os.path.join(keypoint_base, d)) 
                              and d.isdigit()])
    
    logging.info(f"Found {len(numbered_folders)} numbered folders to process: {', '.join(numbered_folders)}")
    print(f"{'=' * 80}")
    
    all_stats = []
    success_count = 0
    skip_count = 0
    error_count = 0
    error_list = []
    
    # Collect all folders to process
    all_tasks = []
    for folder_num in numbered_folders:
        keypoint_folder_base = os.path.join(keypoint_base, folder_num)
        morpheme_folder = os.path.join(morpheme_base, folder_num)
        
        if not os.path.exists(morpheme_folder):
            logging.warning(f"Morpheme folder not found for {folder_num}")
            continue
        
        if not os.path.exists(keypoint_folder_base):
            logging.warning(f"Keypoint folder not found: {keypoint_folder_base}")
            continue
        
        # Find all F view folders in this numbered folder
        try:
            all_folders = sorted([d for d in os.listdir(keypoint_folder_base)
                                if os.path.isdir(os.path.join(keypoint_folder_base, d))])
        except Exception as e:
            logging.error(f"Error listing folder {keypoint_folder_base}: {e}")
            continue
        
        f_folders = [f for f in all_folders if '_F' in f]
        
        logging.info(f"Folder {folder_num}: {len(f_folders)} F-view folders found")
        
        for folder in f_folders:
            keypoint_folder = os.path.join(keypoint_folder_base, folder)
            output_folder_base = os.path.join(output_base, folder_num)
            all_tasks.append((keypoint_folder, morpheme_folder, output_folder_base, dry_run))
    
    logging.info(f"Total {len(all_tasks)} F-view folders to process")
    
    # Process all tasks
    if use_multiprocessing and not dry_run:
        if num_workers is None:
            num_workers = max(1, mp.cpu_count() - 1)
        
        logging.info(f"Using multiprocessing with {num_workers} workers")
        
        with mp.Pool(num_workers) as pool:
            results = list(tqdm(
                pool.imap(process_single_folder_wrapper, all_tasks),
                total=len(all_tasks),
                desc="Processing folders",
                unit="folder"
            ))
    else:
        # Sequential processing with progress bar
        results = []
        for task in tqdm(all_tasks, desc="Processing folders", unit="folder"):
            results.append(process_single_folder_wrapper(task))
    
    # Collect results
    for result in results:
        if result.get('skipped'):
            skip_count += 1
        elif result.get('error'):
            error_count += 1
            folder_name = result.get('folder', 'Unknown')
            error_msg = f"{folder_name}: {result['error']}"
            error_list.append(error_msg)
            logging.error(f"Error processing {error_msg}")
        elif result.get('success'):
            success_count += 1
            all_stats.append(result)
    
    print(f"\n{'=' * 80}")
    print(f"Processing complete!")
    print(f"  Success: {success_count}")
    print(f"  Skipped: {skip_count}")
    print(f"  Errors:  {error_count}")
    
    if all_stats:
        total_original = sum(s['total_frames'] for s in all_stats)
        total_kept = sum(s['kept_frames'] for s in all_stats)
        total_trimmed = sum(s['trimmed_frames'] for s in all_stats)
        
        print(f"\nTotal Statistics:")
        print(f"  Original frames: {total_original:,}")
        print(f"  Kept frames:     {total_kept:,}")
        print(f"  Trimmed frames:  {total_trimmed:,}")
        print(f"  Reduction:       {(total_trimmed/total_original*100):.1f}%")
    
    # Save error log if requested
    if error_log_path and error_list:
        with open(error_log_path, 'w', encoding='utf-8') as f:
            f.write(f"Korean Sign Language Data Preprocessing - Error Log\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'=' * 80}\n")
            f.write(f"Total errors: {len(error_list)}\n\n")
            for error in error_list:
                f.write(f"{error}\n")
        logging.info(f"Error log saved to: {error_log_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Trim Korean Sign Language keypoint data (F view only)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be processed
  python trim_sign_language_data.py --dry-run
  
  # Process with default settings
  python trim_sign_language_data.py
  
  # Process with multiprocessing (faster)
  python trim_sign_language_data.py --multiprocessing --workers 4
  
  # Process with custom paths
  python trim_sign_language_data.py --data-root /path/to/data --output /path/to/output
        """)
    
    parser.add_argument('--data-root', 
                       default='/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets',
                       help='Root directory of the dataset')
    parser.add_argument('--output', 
                       default='/Users/jaylee_83/Documents/_D-ALabs/Data_Sets/SignLanguageSets_Trimmed',
                       help='Output directory for trimmed data')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually copying files')
    parser.add_argument('--error-log',
                       default='preprocessing_errors.log',
                       help='Path to save error log file (default: preprocessing_errors.log)')
    parser.add_argument('--multiprocessing', action='store_true',
                       help='Use multiprocessing for parallel processing (faster)')
    parser.add_argument('--workers', type=int, default=None,
                       help='Number of worker processes (default: CPU count - 1)')
    parser.add_argument('--log-file',
                       default='preprocessing.log',
                       help='Path to save processing log file (default: preprocessing.log)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_file if not args.dry_run else None)
    
    print("=" * 80)
    print("Korean Sign Language Data Preprocessing")
    print("=" * 80)
    print(f"Data root:      {args.data_root}")
    print(f"Output:         {args.output}")
    print(f"Mode:           {'DRY RUN' if args.dry_run else 'PROCESSING'}")
    print(f"Multiprocessing: {'Enabled' if args.multiprocessing else 'Disabled'}")
    if args.multiprocessing and args.workers:
        print(f"Workers:        {args.workers}")
    print(f"Log file:       {args.log_file}")
    print(f"Error log:      {args.error_log}")
    print()
    
    if not os.path.exists(args.data_root):
        logging.error(f"Data root directory not found: {args.data_root}")
        print(f"Error: Data root directory not found: {args.data_root}")
        return
    
    # Verify WORD directory exists
    word_dir = os.path.join(args.data_root, "Training", "Labeled", "REAL", "WORD")
    if not os.path.exists(word_dir):
        logging.error(f"WORD directory not found: {word_dir}")
        print(f"Error: WORD directory not found: {word_dir}")
        return
    
    if not args.dry_run:
        os.makedirs(args.output, exist_ok=True)
        logging.info(f"Output directory created/verified: {args.output}")
    
    # Log start time
    start_time = datetime.now()
    logging.info(f"Processing started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    process_dataset(
        args.data_root, 
        args.output, 
        args.dry_run, 
        args.error_log,
        args.multiprocessing,
        args.workers
    )
    
    # Log end time and duration
    end_time = datetime.now()
    duration = end_time - start_time
    logging.info(f"Processing completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Total duration: {duration}")
    print(f"\nTotal processing time: {duration}")


if __name__ == '__main__':
    main()


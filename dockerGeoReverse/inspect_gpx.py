import gpxpy
import sys
from datetime import timedelta

def analyze_gpx_files(file_paths):
    """
    Analyzes a list of GPX files and prints a summary of their contents.
    """
    print("--- GPX File Inspection ---")
    
    summaries = []
    total_duration = timedelta()

    for file_path in file_paths:
        summary = {
            "file": file_path.split('/')[-1], # Get just the filename
            "points": 0,
            "duration": "N/A",
            "error": None
        }
        try:
            with open(file_path, 'r', encoding='utf-8') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                
                summary["points"] = gpx.get_points_no()
                
                if summary["points"] > 0:
                    duration = gpx.get_duration()

                    if duration is not None:
                        duration_td = timedelta(seconds=duration)
                        summary["duration"] = str(duration_td)
                        total_duration += duration_td
                    else:
                        summary["error"] = "Bevat punten maar GEEN tijdsinformatie."
                else:
                    summary["error"] = "Bestand bevat GEEN GPS-punten."
        except Exception as e:
            summary["error"] = f"Kon bestand niet lezen: {e}"
        
        summaries.append(summary)

    # Print results in a table-like format
    print(f"{'Bestand':<18} | {'Aantal Punten':>15} | {'Duur':>15} | {'Opmerking'}")
    print("-" * 70)
    for s in summaries:
        error_note = s['error'] if s['error'] else "OK"
        print(f"{s['file']:<18} | {s['points']:>15} | {s['duration']:>15} | {error_note}")
        
    print("-" * 70)
    print(f"Berekende totale duur: {total_duration}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_gpx.py <file1.gpx> <file2.gpx> ...")
        sys.exit(1)
        
    files_to_check = sys.argv[1:]
    analyze_gpx_files(files_to_check)
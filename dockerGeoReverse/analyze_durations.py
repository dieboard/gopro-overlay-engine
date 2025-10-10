import sys
import pandas as pd
import gpxpy
from datetime import timedelta

def analyze_files(gpx_filepath, csv_filepath, video_duration_str):
    """
    Analyzes the duration of a GPX and a CSV file and compares them to a video duration.
    """
    results = {}
    
    print("--- Analysis Results ---")
    print(f"Target Video Duration: {video_duration_str}\n")

    # --- 1. Analyze GPX File ---
    try:
        with open(gpx_filepath, 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            start_time_gpx, end_time_gpx = gpx.get_time_bounds()

            if start_time_gpx and end_time_gpx:
                duration_gpx = end_time_gpx - start_time_gpx
                results['gpx'] = {"duration": duration_gpx}
                print("GPX File Analysis:")
                print(f"  Start Time: {start_time_gpx.isoformat()}")
                print(f"  End Time:   {end_time_gpx.isoformat()}")
                print(f"  Total Duration: {duration_gpx}")
            else:
                results['gpx'] = {"error": "No time data found in GPX points."}
                print("GPX File Analysis: No time data found.")
    except Exception as e:
        results['gpx'] = {"error": f"Failed to process GPX file: {e}"}
        print(f"GPX File Analysis: Error - {e}")

    print("-" * 25)

    # --- 2. Analyze CSV File ---
    try:
        df = pd.read_csv(csv_filepath)
        if 'time' in df.columns:
            # GEWIJZIGD: 'format="ISO8601"' toegevoegd om flexibel te zijn met microseconden
            df['time'] = pd.to_datetime(df['time'], format='ISO8601')
            
            start_time_csv = df['time'].min()
            end_time_csv = df['time'].max()
            duration_csv = end_time_csv - start_time_csv
            results['csv'] = {"duration": duration_csv}
            print("CSV File Analysis:")
            print(f"  Start Time: {start_time_csv.isoformat()}")
            print(f"  End Time:   {end_time_csv.isoformat()}")
            print(f"  Total Duration: {duration_csv}")
        else:
            results['csv'] = {"error": "No 'time' column found."}
            print("CSV File Analysis: No 'time' column found.")
    except Exception as e:
        results['csv'] = {"error": f"Failed to process CSV file: {e}"}
        print(f"CSV File Analysis: Error - {e}")
        
    print("\n--- Conclusion ---")
    gpx_ok = 'gpx' in results and 'error' not in results['gpx']
    csv_ok = 'csv' in results and 'error' not in results['csv']
    
    # Parse video duration string H:MM:SS
    h, m, s = map(int, video_duration_str.split(':'))
    video_delta = timedelta(hours=h, minutes=m, seconds=s)

    if not gpx_ok or not csv_ok:
        print("Could not fully analyze both files. Please check the errors above.")
    else:
        duration_gpx = results['gpx']['duration']
        duration_csv = results['csv']['duration']
        
        # Voeg een kleine tolerantie toe (bijv. 2 seconden)
        tolerance = timedelta(seconds=2)
        
        if duration_gpx < (video_delta - tolerance):
            print("Het probleem begint waarschijnlijk bij de GPX-generatie.")
            print(f"De duur van de GPX ({duration_gpx}) is significant korter dan de video ({video_delta}).")
            print("Dit kan gebeuren als het GPS-signaal aan het begin of einde van de opname wegviel.")
        elif duration_csv < (duration_gpx - tolerance):
            print("Het probleem treedt waarschijnlijk op tijdens de CSV-conversie.")
            print(f"De duur van de CSV ({duration_csv}) is significant korter dan de GPX ({duration_gpx}).")
            print("Dit wordt vaak veroorzaakt door filters (zoals --only-locked) die punten met een slecht GPS-signaal verwijderen.")
        else:
            print("De duur van de GPX- en CSV-bestanden komt overeen met de videoduur.")
            print("Het probleem zit dan mogelijk in het script dat de overlay genereert, niet in de databestanden.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 analyze_durations.py <gpx_file_path> <csv_file_path> <video_duration H:MM:SS>")
        sys.exit(1)
        
    gpx_path = sys.argv[1]
    csv_path = sys.argv[2]
    video_duration = sys.argv[3]
    
    analyze_files(gpx_path, csv_path, video_duration)
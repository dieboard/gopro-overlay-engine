import gpxpy
import gpxpy.gpx
import argparse
from datetime import timedelta

def merge_gpx_files(output_file, *gpx_files):
    """
    Merges multiple GPX files and removes the time gaps between them.
    """
    merged_gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    merged_gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    last_timestamp = None
    total_duration = timedelta()

    print(f"Merging {len(gpx_files)} GPX files...")

    for i, file_path in enumerate(gpx_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

                if not gpx.tracks:
                    print(f"Warning: {file_path} contains no tracks. Skipping.")
                    continue

                print(f"Processing '{file_path}'...")
                
                all_points = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
                
                if not all_points:
                    print(f"Warning: {file_path} contains no points. Skipping.")
                    continue

                # --- FIX IS HERE ---
                # Use the get_duration() method, which returns seconds
                file_duration_seconds = gpx.get_duration()
                if file_duration_seconds is None:
                    file_duration_seconds = 0
                
                total_duration += timedelta(seconds=file_duration_seconds)
                # --- END OF FIX ---

                if i == 0:
                    gpx_segment.points.extend(all_points)
                    last_timestamp = all_points[-1].time
                else:
                    current_start_time = all_points[0].time
                    # Add a small buffer of 1 second to the gap to ensure continuity
                    time_gap = current_start_time - (last_timestamp + timedelta(seconds=1))

                    print(f"  Detected time gap. Adjusting timestamps by {time_gap}...")
                    
                    adjusted_points = []
                    for point in all_points:
                        point.time -= time_gap
                        adjusted_points.append(point)
                    
                    gpx_segment.points.extend(adjusted_points)
                    last_timestamp = adjusted_points[-1].time

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'. Skipping.")
        except Exception as e:
            print(f"An error occurred processing '{file_path}': {e}. Skipping.")

    print(f"\nWriting merged GPX to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_gpx.to_xml())
        
    print(f"Merge complete! Final calculated duration: {total_duration}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple GPX files and remove time gaps.")
    parser.add_argument('gpx_files', nargs='+', help="Paths to the GPX files to merge, in order.")
    parser.add_argument('-o', '--output', required=True, help="Path for the merged output GPX file.")
    
    args = parser.parse_args()
    
    merge_gpx_files(args.output, *args.gpx_files)
import gpxpy
import gpxpy.gpx
import argparse
from datetime import timedelta

def merge_gpx_files(output_file, *gpx_files):
    """
    Merges multiple GPX files intelligently by creating a continuous timeline.
    """
    merged_gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    merged_gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # This will keep track of the end time of the last point added.
    timeline_cursor = None

    print(f"Merging {len(gpx_files)} GPX files with new logic...")

    for file_path in gpx_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                print(f"Processing '{file_path}'...")

                all_points = [point for track in gpx.tracks for segment in track.segments for point in segment.points]

                if not all_points:
                    print(f"  -> Warning: File contains no points. Skipping.")
                    continue

                first_point_time_in_file = all_points[0].time

                # If this is the first file, the timeline starts with its first point.
                if timeline_cursor is None:
                    timeline_cursor = first_point_time_in_file
                
                # Add a 1-second gap between clips for clarity
                timeline_cursor += timedelta(seconds=1)

                for point in all_points:
                    # Calculate how far into its own timeline this point is
                    delta_from_start = point.time - first_point_time_in_file
                    
                    # Apply that delta to our continuous timeline cursor
                    point.time = timeline_cursor + delta_from_start
                    
                    # Add the adjusted point to our new, merged segment
                    gpx_segment.points.append(point)

                # After processing all points in a file, update the cursor to the last point's time
                if gpx_segment.points:
                    timeline_cursor = gpx_segment.points[-1].time

        except Exception as e:
            print(f"  -> An error occurred processing '{file_path}': {e}. Skipping.")

    print(f"\nWriting merged GPX to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_gpx.to_xml())
        
    print("Merge complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple GPX files and remove time gaps.")
    parser.add_argument('gpx_files', nargs='+', help="Paths to the GPX files to merge, in order.")
    parser.add_argument('-o', '--output', required=True, help="Path for the merged output GPX file.")
    
    args = parser.parse_args()
    
    merge_gpx_files(args.output, *args.gpx_files)
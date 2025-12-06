import gpxpy
import gpxpy.gpx
import argparse
from datetime import timedelta

def merge_gpx_files(output_file, *gpx_files):
    """
    Merges multiple GPX files intelligently by creating a continuous timeline.
    It clamps large gaps between points (both within and between files) to prevent
    date jumps caused by bad GPS data or long pauses.
    """
    merged_gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    merged_gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # This will keep track of the end time of the last point added.
    timeline_cursor = None

    # Threshold for what constitutes a "large gap" that should be closed.
    # 60 seconds is reasonable for GoPro clips.
    # If the gap is larger, we reset it to a small step.
    MAX_GAP_SECONDS = 60
    DEFAULT_STEP = timedelta(seconds=1)

    print(f"Merging {len(gpx_files)} GPX files with incremental gap logic...")

    for file_path in gpx_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                print(f"Processing '{file_path}'...")

                all_points = [point for track in gpx.tracks for segment in track.segments for point in segment.points]

                if not all_points:
                    print(f"  -> Warning: File contains no points. Skipping.")
                    continue

                # Initialize timeline_cursor with the start of the first file if needed
                if timeline_cursor is None:
                    # For the very first point of the very first file, we keep its original time.
                    timeline_cursor = all_points[0].time
                    # We subtract a small amount so the loop logic adds the step correctly?
                    # Actually, let's just handle the first point specially in the loop.
                    # But simpler: set cursor to T0 - step.
                    timeline_cursor -= DEFAULT_STEP

                # Track previous original time to calculate gaps within the file
                previous_original_time = None

                # Add a mandatory gap between files (handled by the loop logic if we treat it as a stream)
                # But we want to ENFORCE a gap between files regardless of original timestamps.
                # The logic below will calculate `gap = current - previous`.
                # If we are starting a NEW file, `previous_original_time` is None.

                for point in all_points:
                    original_time = point.time

                    if previous_original_time is None:
                        # First point of the file.
                        # We force a small step from the previous file's end (timeline_cursor).
                        # Effectively closing the gap between files to DEFAULT_STEP.
                        gap = DEFAULT_STEP
                    else:
                        # Calculate gap from previous point in THIS file
                        gap = original_time - previous_original_time

                        # Check for huge gaps (bad data or pauses)
                        if gap.total_seconds() > MAX_GAP_SECONDS:
                            print(f"  -> Detected large gap ({gap}) at {original_time}. Clamping to {DEFAULT_STEP}.")
                            gap = DEFAULT_STEP
                        elif gap.total_seconds() < 0:
                            # Negative gap (time going backwards), clamp to 0 or small step
                             print(f"  -> Detected negative gap ({gap}) at {original_time}. Clamping to 0s.")
                             gap = timedelta(seconds=0)
                    
                    # Apply the gap to the timeline
                    new_time = timeline_cursor + gap
                    point.time = new_time
                    
                    # Update cursors
                    timeline_cursor = new_time
                    previous_original_time = original_time

                    # Add point
                    gpx_segment.points.append(point)

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

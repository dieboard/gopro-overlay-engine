import inspect
import sys
from functools import wraps
from pathlib import Path

import pytest
from PIL import ImageChops, Image, ImageStat

from tests.testenvironment import is_ci


def approve_image(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        function_name = f.__name__
        sourcefile = Path(inspect.getfile(f))

        approval_dir = sourcefile.parents[0].joinpath("approvals")

        approval_stem = f"{sourcefile.stem}_{function_name.replace('test_', '')}"
        approved_location = approval_dir.joinpath(f"{approval_stem}.approved.png")
        actual_location = approval_dir.joinpath(f"{approval_stem}.actual.png")
        diff_location = approval_dir.joinpath(f"{approval_stem}.diff.png")
        approved_diff_location = approval_dir.joinpath(f"{approval_stem}.diff_over_approved.png")

        actual_image = f(*args, **kwargs)

        if is_ci():
            # Image output isn't stable on CI, nor outside of PyCharm :-(
            return

        if actual_image is None:
            raise AssertionError(f"{function_name} needs to return the image it created")

        actual_image.save(actual_location, "PNG")
        if not approved_location.exists():
            print(f"cp {actual_location} {approved_location}", file=sys.stderr)
            pytest.xfail(f"{function_name}: approved File does not exist, no assertion")

        else:
            approved_image = Image.open(approved_location)
            difference = ImageChops.difference(actual_image, approved_image)
            stat = ImageStat.Stat(difference)
            total_difference = sum(stat.sum)
            diff_location.unlink(missing_ok=True)
            approved_diff_location.unlink(missing_ok=True)
            if total_difference > 0.0:

                for x in range(0, approved_image.width):
                    for y in range(0, approved_image.height):
                        approved_pixel = approved_image.getpixel((x, y))
                        actual_pixel = actual_image.getpixel((x, y))
                        if approved_pixel != actual_pixel:
                            difference.putpixel((x, y), (255, 0, 0, 255))
                            approved_image.putpixel((x, y), (255, 0, 0, 255))

                difference.save(diff_location, "PNG")
                approved_image.save(approved_diff_location, "PNG")

                approved_image.show()

                print(f"{function_name}: failed approval", file=sys.stderr)
                print(f"Approved {approved_location}", file=sys.stderr)
                print(f"Actual {actual_location}", file=sys.stderr)
                print(f"Diff {diff_location}", file=sys.stderr)
                print(f"Differences by channel {stat.sum}", file=sys.stderr)
                print(f"If this is OK....", file=sys.stderr)
                print(f"cp {actual_location} {approved_location}", file=sys.stderr)
                raise AssertionError("Actual and Approved do not match")

    return wrapper


def approve_text(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        function_name = f.__name__
        sourcefile = Path(inspect.getfile(f))

        approval_dir = sourcefile.parents[0].joinpath("approvals")

        approval_stem = f"{sourcefile.stem}_{function_name.replace('test_', '')}"
        approved_location = approval_dir.joinpath(f"{approval_stem}.approved.txt")
        actual_location = approval_dir.joinpath(f"{approval_stem}.actual.txt")

        actual_text = f(*args, **kwargs)

        if actual_text is None:
            raise AssertionError(f"{function_name} needs to return some text")

        actual_location.write_text(actual_text)

        if approved_location.exists():
            approved_text = approved_location.read_text()

            if not actual_text == approved_text:
                print(f"If this is OK....", file=sys.stderr)
                print(f"cp {actual_location} {approved_location}", file=sys.stderr)
                raise AssertionError("Actual and Approved do not match")
        else:
            print(f"cp {actual_location} {approved_location}", file=sys.stderr)
            pytest.xfail(f"{function_name}: approved File does not exist, no assertion")
    return wrapper
import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README-PYPI.md").read_text()

requires = [
    "pillow==10.1.0",
    "pint==0.22",
    "geotiler==0.15",
    "gpxpy==1.6.1",
    "fitdecode==0.10.0",
    "geographiclib==1.52",
    "progressbar2==4.2.0",
    "requests==2.31.0",
    "sqlitedict==2.1.0",
    "haversine==2.8.0",
]

test_requirements = [
    "pytest"
]

setup(
    name="gopro-overlay",
    version="0.129.0",
    description="Overlay graphics dashboards onto GoPro footage, or create videos from GPX or FIT files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dieboard/gopro-overlay-engine",
    author="DieBoard",
    author_email="DieBoard@github.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
    ],
    packages=[
        "gopro_overlay",
        "gopro_overlay.gpmf",
        "gopro_overlay.gpmf.visitors",
        "gopro_overlay.icons",
        "gopro_overlay.layouts",
        "gopro_overlay.widgets",
        "gopro_overlay.widgets.cairo",
        "gopro_overlay.layout_components",
    ],
    install_requires=requires,
    tests_require=test_requirements,
    python_requires=">=3.10",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "gopro-contrib-data-extract=bin.gopro-contrib-data-extract:main",
            "gopro-cut=bin.gopro-cut:main",
            "gopro-dashboard=bin.gopro-dashboard:main",
            "gopro-extract=bin.gopro-extract:main",
            "gopro-join=bin.gopro-join:main",
            "gopro-layout=bin.gopro-layout:main",
            "gopro-rename=bin.gopro-rename:main",
            "gopro-to-csv=bin.gopro-to-csv:main",
            "gopro-to-gpx=bin.gopro-to-gpx:main",
            "gopro-debug=bin.gopro-debug:main",
        ]
    },
    project_urls={
        'Source': 'https://github.com/dieboard/gopro-overlay-engine',
    },
)

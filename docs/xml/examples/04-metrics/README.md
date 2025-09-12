<!-- 

Auto Generated File DO NOT EDIT 

-->
# Metrics

Metrics are fields that are extracted or derived from the GoPro or GPX data.

The metric component draws the value of a bit of data on the screen at the given co-ordinate.


```xml
<component type="metric" metric="speed" />
```
<kbd>![04-metrics-0.png](04-metrics-0.png)</kbd>


## Conversions

Every metric knows its units, and can be converted to another unit easily. See [below](#supported-metrics) for the base unit
for each metric.


```xml
<component type="metric" metric="speed" />
```
<kbd>![04-metrics-1.png](04-metrics-1.png)</kbd>


```xml
<component type="metric" metric="speed" units="kph" />
```
<kbd>![04-metrics-2.png](04-metrics-2.png)</kbd>


```xml
<component type="metric" metric="speed" units="mph" />
```
<kbd>![04-metrics-3.png](04-metrics-3.png)</kbd>


```xml
<component type="metric" metric="speed" units="knots" />
```
<kbd>![04-metrics-4.png](04-metrics-4.png)</kbd>



```xml
<component type="metric" metric="speed" units="pace_km" />
```
<kbd>![04-metrics-5.png](04-metrics-5.png)</kbd>



The following units are supported:

| Dimension                        | Units                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------|
| Speed                            | mph, kph, mps (metres-per-second), fps (feet-per-second), knots, knot,              |
| Pace (Minutes per distance-unit) | pace, pace_km, pace_mile, pace_kt                             | 
| Temperature                      | degreeF, degreeC, degreeK                                                           |
| Distance                         | mile, miles, m, metres, km, nmi (nautical mile), foot, yard, hand, angstrom, parsec |
| Acceleration                     | gravity, G, m/s^2, m/s²                                                             |
| Power                            | W, kW, watt, hp (UK horsepower)                                                     |
| Rotation                         | degrees, radians                                                                    |

`gravity` and `G` are synonyms for 9.80665 m/s², so will convert acceleration values to G's

Conversions that don't make sense for a given metric will fail with a suitable message.

## Controllable units

Some units can be controlled by the command line, so instead of using a particular unit, you can also use on eof the following

| Unit          | Meaning                            |
|---------------|------------------------------------|
| `speed`       | User-controllable speed unit       |
| `distance`    | User-controllable distance unit    |
| `temperature` | User-controllable temperature unit |
| `altitude`    | User-controllable altitude unit    |

Using these units, along with the `metric-unit` component, means that a single layout can serve for UK, EU and US measurements, or mixed unit layouts 
like distances in km, but altitude in feet (to give higher numbers if you are cycling!)


```xml
<component type="metric"      y="0" metric="speed" units="speed" dp="0" />
<component type="metric-unit" y="32" metric="speed" units="speed">Using {:P} </component>
<component type="metric-unit" y="64" metric="speed" units="speed">Using {:~P} </component>
```
<kbd>![04-metrics-6.png](04-metrics-6.png)</kbd>




## Lat & Lon

GPS Location is just another metric...

`cache="false"` is suggested for lat & lon metrics, as they will rarely repeat. By default text glyphs are cached, as they are
quite slow to render. This can be ignored really unless there are memory errors while rendering.


```xml
<component type="metric" metric="lat" dp="6" size="16" cache="false"/>
```
<kbd>![04-metrics-7.png](04-metrics-7.png)</kbd>


## Formatting

Either a number of decimal places, or a specific python formatting string can be used, or the word "pace"

### Decimal Places

use the `dp` attribute


```xml
<component type="metric" metric="speed" dp="0" />
```
<kbd>![04-metrics-8.png](04-metrics-8.png)</kbd>


```xml
<component type="metric" metric="speed" dp="2" />
```
<kbd>![04-metrics-9.png](04-metrics-9.png)</kbd>


```xml
<component type="metric" metric="speed" dp="5" />
```
<kbd>![04-metrics-10.png](04-metrics-10.png)</kbd>


### Format string

Use the `format` attribute.


```xml
<component type="metric" metric="speed" format=".4f" />
```
<kbd>![04-metrics-11.png](04-metrics-11.png)</kbd>



### Pace

A special case for formatting pace.


```xml
<component type="metric" metric="speed" units="pace" format="pace" />
```
<kbd>![04-metrics-12.png](04-metrics-12.png)</kbd>


## Positioning

The same positioning as in the [text](01-simple-text.md) component


```xml
<component type="metric" x="40" metric="speed" />
```
<kbd>![04-metrics-13.png](04-metrics-13.png)</kbd>


## Alignment

The same alignment as in the [text](01-simple-text.md) component


```xml
<component type="metric" x="40" metric="speed" align="right" />
```
<kbd>![04-metrics-14.png](04-metrics-14.png)</kbd>


## Colour

The same colour as in the [text](01-simple-text.md) component


```xml
<component type="metric" metric="speed" rgb="255,255,0" />
```
<kbd>![04-metrics-15.png](04-metrics-15.png)</kbd>


```xml
<component type="metric" metric="speed" rgb="255,255,0,128" />
```
<kbd>![04-metrics-16.png](04-metrics-16.png)</kbd>


```xml
<component type="metric" metric="speed" rgb="255,0,0" outline="255,255,255" size="48" />
```
<kbd>![04-metrics-17.png](04-metrics-17.png)</kbd>


```xml
<component type="metric" metric="speed" rgb="255,0,0" outline="255,255,255" outline_width="5" size="48"  />
```
<kbd>![04-metrics-18.png](04-metrics-18.png)</kbd>


## Supported Metrics

The following metrics are supported:
`hr`, `cadence`, `speed`, `cspeed`, `temp`,
`gradient`, `alt`, `odo`, `dist`, `azi`, `lat`, `lon`, `accl.x`, `accl.y`, `accl.z`, `grav.x`,
`grav.y`, `grav.z`, `ori.pitch`, `ori.roll`, `ori.yaw`

Currently, there is no mechanism to calculate the overall acceleration, this will come in a future version.

| Metric    | Source | Description                                                       | Unit |
|-----------|-------|-------------------------------------------------------------------|----------------------|
| hr        | gpx      fit | Heart Rate                                                        | beats / minute |
| cadence   | gpx      fit | Cadence                                                           | revolutions / minute |
| power     | gpx      fit | Power                                                             | watts |
| speed     | gopro gpx fit | Speed (as reported by device if available, or fallback to cspeed) | metres / second |
| cspeed    | gopro gpx fit | Computed Speed  (derived from location delta)                     | metres / second |
| temp      | gpx       fit | Ambient Temperature                                               | degrees C |
| gradient  | gopro gpx fit | Gradient of Ascent                                                | - |
| alt       | gopro gpx fit | Height above sea level                                            | metres |
| odo       | gopro gpx fit | Distance since start                                              | metres |
| dist      | gopro gpx fit | Distance since last point                                         | metres |
| azi       | gopro gpx fit | Azimuth                                                           | degree |
| cog       | gopro gpx fit | Course over Ground                                                | degree |
| lat       | gopro gpx fit | Latitude                                                          | - |
| lon       | gopro gpx fit | Longitude                                                         | - |
| accel     | gopro gpx fit | Acceleration - Computed from speed                                | m/s² |
| accl.x    | gopro | Acceleration - X Axis                                             | m/s² |
| accl.y    | gopro | Acceleration - Y Axis                                             | m/s² |
| accl.z    | gopro | Acceleration - Z Axis                                             | m/s² |
| grav.x    | gopro | Gravity Vector - X Axis                                           | - |
| grav.y    | gopro | Gravity Vector - Y Axis                                           | - |
| grav.z    | gopro | Gravity Vector - Z Axis                                           | - |
| ori.pitch | gopro | Orientation - Pitch                                               | radians |
| ori.roll  | gopro | Orientation - Roll                                                | radians |
| ori.yaw   | gopro | Orientation - Yaw                                                 | radians |
| respiration | fit   | Respiration Rate | brpm / brps - Breaths Per Minute / Second |
| gear.front | fit   | Front Gear Number | - |
| gear.rear | fit   | Rear Gear Number | - |
| sdps | fit | Sensor Distance Per Stroke ( Vaaka Cadence Sensor ) | cm |

# Axes of Acceleration & Rotation

Image (C) GoPro - from https://github.com/gopro/gpmf-parser

![GoPro IMU Orientation](https://github.com/gopro/gpmf-parser/raw/main/docs/readmegfx/CameraIMUOrientationSM.png)


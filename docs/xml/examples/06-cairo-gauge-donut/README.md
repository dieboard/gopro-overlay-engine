<!-- 

Auto Generated File DO NOT EDIT 

-->
<!-- Dimension(256,256) -->

# Cairo Gauge Donut

_Requires Cairo to be installed_

Shows a gauge which is some sector of a donut..

Any supported metric or unit can be used


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph" />
```
<kbd>![06-cairo-gauge-donut-0.png](06-cairo-gauge-donut-0.png)</kbd>


# Size

Use `size` to change the size.

# Max and Min Values

Use `max` and `min` to set maximum and minimum values.


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  />
```
<kbd>![06-cairo-gauge-donut-1.png](06-cairo-gauge-donut-1.png)</kbd>


# Rotation and Length

The gauge by default starts at the bottom left, this can be changed using `start`, which is the number of degrees to rotate clockwise. The default `start` is 143.


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  start="270"/>
```
<kbd>![06-cairo-gauge-donut-2.png](06-cairo-gauge-donut-2.png)</kbd>


The gauge is normally 254 degrees "long". This can be changed using `length`


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="90" />
```
<kbd>![06-cairo-gauge-donut-3.png](06-cairo-gauge-donut-3.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="180" />
```
<kbd>![06-cairo-gauge-donut-4.png](06-cairo-gauge-donut-4.png)</kbd>


You can use -ve length to make the gauge draw anti-clockwise


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="-90" />
```
<kbd>![06-cairo-gauge-donut-5.png](06-cairo-gauge-donut-5.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="-180" />
```
<kbd>![06-cairo-gauge-donut-6.png](06-cairo-gauge-donut-6.png)</kbd>



# Number of Ticks / Sectors

There are 5 sectors by default. This can be changed with `sectors`


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="90" sectors="20" />
```
<kbd>![06-cairo-gauge-donut-7.png](06-cairo-gauge-donut-7.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="180" sectors="6" />
```
<kbd>![06-cairo-gauge-donut-8.png](06-cairo-gauge-donut-8.png)</kbd>


# Range Markers

You can set range markers, like the`cairo-gauge-arc-annotated` widget.


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  length="180" sectors="6" max="60" arc-value-upper="60" arc-value-lower="50" arc-inner-rgb="255,0,255,50" arc-outer-rgb="255,0,0,250" />
```
<kbd>![06-cairo-gauge-donut-9.png](06-cairo-gauge-donut-9.png)</kbd>


# Colours

Various colours can be set, either as RGB, or RGBA values.

The following are available to change: `background-inner-rgb`, `background-outer-rgb`, `major-ann-rgb`, `minor-ann-rgb`, `needle-rgb`, `major-tick-rgb`, `minor-tick-rgb`, `arc-inner-rgb`, `arc-outer-rgb`


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  background-inner-rgb="255,0,0"/>
```
<kbd>![06-cairo-gauge-donut-10.png](06-cairo-gauge-donut-10.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  background-outer-rgb="0,255,0"/>
```
<kbd>![06-cairo-gauge-donut-11.png](06-cairo-gauge-donut-11.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  major-ann-rgb="255,0,0"/>
```
<kbd>![06-cairo-gauge-donut-12.png](06-cairo-gauge-donut-12.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  minor-ann-rgb="255,0,0"/>
```
<kbd>![06-cairo-gauge-donut-13.png](06-cairo-gauge-donut-13.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  major-tick-rgb="255,0,0"/>
```
<kbd>![06-cairo-gauge-donut-14.png](06-cairo-gauge-donut-14.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  minor-tick-rgb="255,0,0"/>
```
<kbd>![06-cairo-gauge-donut-15.png](06-cairo-gauge-donut-15.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  needle-rgb="255,0,255"/>
```
<kbd>![06-cairo-gauge-donut-16.png](06-cairo-gauge-donut-16.png)</kbd>


# Transparency

Any colour that is completely transparent will disappear... this can be used to change the appearance of the widget quite a bit.


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  background-inner-rgb="255,0,0,0"/>
```
<kbd>![06-cairo-gauge-donut-17.png](06-cairo-gauge-donut-17.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  major-ann-rgb="255,0,0,0"/>
```
<kbd>![06-cairo-gauge-donut-18.png](06-cairo-gauge-donut-18.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  minor-ann-rgb="255,0,0,0"/>
```
<kbd>![06-cairo-gauge-donut-19.png](06-cairo-gauge-donut-19.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  major-tick-rgb="255,0,0,0"/>
```
<kbd>![06-cairo-gauge-donut-20.png](06-cairo-gauge-donut-20.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  minor-tick-rgb="255,0,0,0"/>
```
<kbd>![06-cairo-gauge-donut-21.png](06-cairo-gauge-donut-21.png)</kbd>


```xml
<component type="cairo-gauge-donut" metric="speed" units="mph"  needle-rgb="255,0,255,40"/>
```
<kbd>![06-cairo-gauge-donut-22.png](06-cairo-gauge-donut-22.png)</kbd>



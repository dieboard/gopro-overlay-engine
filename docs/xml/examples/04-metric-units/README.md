<!-- 

Auto Generated File DO NOT EDIT 

-->
# Metric Units

Some of the units in the layout can be changed using the command line. For example,
running `gopro-dashboard.py` with `--units-speed kph` will result in the default dashboard
showing the speeds in KPH.

To display the correct text for units, we can use the `metric-unit` component. It is a little bit like a `text`
component.

There are some formatting controls that will be replaced with the relevant unit. This works for all 
units, including some of the more complex ones, like acceleration.

## Formatting 

A formatting command can be placed inside braces `{}`. Formatting commands are one of

- `C` Compact
- `P` Pretty
- `D` Default
- `c` Compact - Upper Case
- `p` Pretty - Upper Case
- `d` Default - Upper Case

Yes, the upper and lower case things are a bit back-to-front.

Also, the following character can be used, in addition

- `~` - Use unit symbol, not name

## Examples


```xml
<component type="metric-unit" metric="speed" units="speed">Speed in {:C}</component>
```
<kbd>![04-metric-units-0.png](04-metric-units-0.png)</kbd>


```xml
<component type="metric-unit" metric="accl.x" >Acceleration in {:C}</component>
```
<kbd>![04-metric-units-1.png](04-metric-units-1.png)</kbd>



```xml
<component type="metric-unit" metric="speed" units="speed">Speed in {:~C}</component>
```
<kbd>![04-metric-units-2.png](04-metric-units-2.png)</kbd>


```xml
<component type="metric-unit" metric="accl.x" >Acceleration in {:~C}</component>
```
<kbd>![04-metric-units-3.png](04-metric-units-3.png)</kbd>



```xml
<component type="metric-unit" metric="speed" units="speed">Speed in {:~P}</component>
```
<kbd>![04-metric-units-4.png](04-metric-units-4.png)</kbd>


```xml
<component type="metric-unit" metric="accl.x" >Acceleration in {:~P}</component>
```
<kbd>![04-metric-units-5.png](04-metric-units-5.png)</kbd>


## 

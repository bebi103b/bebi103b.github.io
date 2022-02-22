import numpy as np

import bokeh.plotting
from bokeh.io import curdoc,output_notebook,show
import bokeh.palettes
from bokeh.models import Slider, Button
from bokeh.layouts import row,layout
import holoviews as hv
renderer = hv.renderer('bokeh')

hv.extension('bokeh')
output_notebook()


def q(t, ω=2*np.pi/30, ϕ_0=np.pi/2):
    return np.sin(ω * t + ϕ_0)

def p(t, ω=2*np.pi/30, ϕ_0=np.pi/2):
    return np.cos(ω * t + ϕ_0)


def make_plot(t):
    spring = hv.Scatter(([q(t)], [0])).opts(xlabel='q', size=6, show_grid=True, title="Spring")
    phase_space = hv.Scatter(([q(t)], [p(t)])).opts(xlabel="q", ylabel='p', size=6, show_grid=True, title="Phase Space")
    trajectory = hv.Path(([q(_t) for _t in np.linspace(0, 30, 200)], [p(_t) for _t in np.linspace(0, 30, 200)])).opts(xlabel="q", ylabel='p(x)', line_width=2, color="orange")
    return (spring+ (phase_space * trajectory)).opts(shared_axes=False)
    
x = np.arange(0, 30)

trace = hv.HoloMap({t: make_plot(t)  for t in x})

# Convert the HoloViews object into a plot
plot = renderer.get_plot(trace)



def animate_update():
    time = slider.value + 1
    if time >= 30:
        time = 0
    slider.value = time

def slider_update(attrname, old, new):
    plot.update(slider.value)
    
slider = Slider(start=0, end=30, value=0, step=1, title="t")
slider.on_change('value', slider_update)


# Combine the bokeh plot on plot.state with the widgets
layout = layout([
    [plot.state],
    [slider]
], sizing_mode='fixed')

curdoc().add_root(layout)

curdoc().add_periodic_callback(animate_update, 1)
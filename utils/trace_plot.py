import scipy
import pylab
import matplotlib.pylab as plt
import numpy as np

from scipy.fft import fft, ifft
from IPython.display import display

def plot_scope_traces(scope, traces_data, time_axis=True):
    """Plots scope output traces for examination using matplotlib.

    Used in jupyter with the `%matplotlib ipympl` magic keywork
    
    Args:
    	scope (object): chipwhisperer scope object
    	traces_data (tuple(list(any), str, optional(str))): trace to be plotted
    	time_axis (bool): If true, converts x-axis from sample index to time-axis using adc conversion.
    
    Returns:
    	none: renders plots on output
    """
    x_domain = np.arange(scope.adc.samples)
    
    if time_axis:
        x_domain = (time_domain / scope.clock.adc_freq) * (1e6)

    render_traces(x_domain, traces_data)

def plot_traces(x_domain, traces_data):
    """Plots generated output traces for examination using matplotlib.
        
    Used in jupyter with the `%matplotlib ipympl` magic keywork
    
    Args:
    	x_domain (list(any)): create 
    	traces_data (tuple(list(any), str, optional(str))): trace to be plotted
    
    Returns:
    	none: renders plots on output
    """
    render_traces(x_domain, traces_data)
    
def render_traces(x_domain, y_domain, title="Traces", x_axis_label="Input", y_axis_label="Output"):
    """Renders generated output traces for examination using matplotlib.
        
    Used in jupyter with the `%matplotlib ipympl` magic keywork
    
    Args:
    	x_domain (list(int)): x-domain values
    	y_domain (list(any)): normal contains tuple of values to be plotted
    
    Returns:
    	none: renders plots on output
    """
    plt.clf()
    fig, ax = plt.subplots(figsize=(15,5))

    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    ax.grid(True)

    legend_exists = True

    plotted_traces = []

    for trace, description, *color in y_domain:
        legend_exists = legend_exists and description != ""
        plotted_trace, = ax.plot(x_domain, trace, label=description, color=color[0])
        plotted_traces.append(plotted_trace)

    if not legend_exists:
        plt.show()
        return
        
    leg = ax.legend(ncol=16, loc='center', bbox_to_anchor=(0.8, 0.2), fontsize='small', columnspacing=1)
    lined = {}

    for legline, origline in zip(leg.get_lines(), plotted_traces):
        legline.set_picker(True)  # Enable picking
        lined[legline] = origline

    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)  # fade legend entry
        fig.canvas.draw()

    fig.canvas.mpl_connect("pick_event", on_pick)
    plt.show()

def plot_trace_FFT(scope, trace_data):
    plt.clf()

    (trace, description) = trace_data
    time_domain = (np.arange(scope.adc.samples) / scope.clock.adc_freq) * (1e6)
    trace_FFT = abs(fft(trace))
    freqs = scipy.fftpack.fftfreq(trace.size, time_domain[1]-time_domain[0])
    
    pylab.subplot(211)
    pylab.plot(time_domain, trace)
    pylab.subplot(212)
    pylab.plot(freqs,20*np.log10(trace_FFT),'x')
    pylab.show()

def plot_reset():
    plt.close('all')
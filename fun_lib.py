import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque


def plot_simple_car(trajectory, par):
    t = np.arange(0, par['t_stop'], par['dt'])  # create a time array from 0..t_stop sampled at 0.02 second steps
    history_len = int(par['t_stop'] / par['dt'])  # how many trajectory points to display

    x1 = trajectory[:, 0]
    y1 = trajectory[:, 2]

    fig = plt.figure(figsize=(10, 4))
    gs = gridspec.GridSpec(2, 2)
    ax1 = fig.add_subplot(gs[:, 0], autoscale_on=False, xlim=(-5.0, 5.0), ylim=(-5.0, 5.0))
    ax1.set_aspect('equal')
    ax1.grid()
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.annotate('Target',
                xy=(0, 0), xycoords='data',
                xytext=(35, 5), textcoords='offset points',
                horizontalalignment='right', verticalalignment='bottom')

    line, = ax1.plot(0, 0, '+', ms=15.0, mec='k')
    line, = ax1.plot([], 'o-', lw=2, c='r')
    trace, = ax1.plot([], ',-', lw=1, c='b')
    time_template = 'time = %.1fs'
    time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)
    history_x, history_y, history_t = deque(maxlen=history_len), deque(maxlen=history_len), deque(maxlen=history_len)

    ax2 = fig.add_subplot(gs[0, 1], autoscale_on=False, xlim=(0.0, par['t_stop']), ylim=(-5.0, 5.0))
    line2, = ax2.plot([], 'o-', lw=2, c='r')
    trace2, = ax2.plot([], ',-', lw=1, c='b')
    ax2.grid()
    ax2.set_xlabel('time')
    ax2.set_ylabel('x')

    ax3 = fig.add_subplot(gs[1, 1], autoscale_on=False, xlim=(0.0, par['t_stop']), ylim=(-5.0, 5.0))
    line3, = ax3.plot([], 'o-', lw=2, c='r')
    trace3, = ax3.plot([], ',-', lw=1, c='b')
    ax3.grid()
    ax3.set_xlabel('time')
    ax3.set_ylabel('y')

    def animate(i):
        thisx = [x1[i]]
        thisy = [y1[i]]
        thist = i * par['dt']

        if i == 0:
            history_x.clear()
            history_y.clear()
            history_t.clear()

        history_x.appendleft(thisx[0])
        history_y.appendleft(thisy[0])
        history_t.appendleft(thist)

        line.set_data(thisx, thisy)
        trace.set_data(history_x, history_y)
        time_text.set_text(time_template % (i * par['dt']))

        line2.set_data(thist, thisx)
        trace2.set_data(history_t, history_x)

        line3.set_data(thist, thisy)
        trace3.set_data(history_t, history_y)

        return line, trace, time_text, line2, trace2, line3, trace3

    ani = animation.FuncAnimation(fig, animate, len(trajectory), interval=par['dt']*1000, blit=True)
    return ani


def plot_and_save_simple_car(trajectory, par):
    t = np.arange(0, par['t_stop'], par['dt'])  # create a time array from 0..t_stop sampled at 0.02 second steps
    history_len = int(par['t_stop'] / par['dt'])  # how many trajectory points to display

    x1 = trajectory[:, 0]
    y1 = trajectory[:, 2]

    fig = plt.figure(figsize=(5, 4))
    gs = gridspec.GridSpec(2, 2)
    ax1 = fig.add_subplot(autoscale_on=False, xlim=(-5.0, 5.0), ylim=(-5.0, 5.0))
    ax1.set_aspect('equal')
    ax1.grid()
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.annotate('Target',
                xy=(0, 0), xycoords='data',
                xytext=(35, 5), textcoords='offset points',
                horizontalalignment='right', verticalalignment='bottom')

    line, = ax1.plot(0, 0, '+', ms=15.0, mec='k')
    line, = ax1.plot([], 'o-', lw=2, c='r')
    trace, = ax1.plot([], ',-', lw=1, c='b')
    time_template = 'time = %.1fs'
    time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)
    history_x, history_y, history_t = deque(maxlen=history_len), deque(maxlen=history_len), deque(maxlen=history_len)


    def animate(i):
        thisx = [x1[i]]
        thisy = [y1[i]]
        thist = i * par['dt']

        if i == 0:
            history_x.clear()
            history_y.clear()
            history_t.clear()

        history_x.appendleft(thisx[0])
        history_y.appendleft(thisy[0])
        history_t.appendleft(thist)

        line.set_data(thisx, thisy)
        trace.set_data(history_x, history_y)
        time_text.set_text(time_template % (i * par['dt']))
        return line, trace, time_text

    ani = animation.FuncAnimation(fig, animate, len(trajectory), interval=par['dt']*1000, blit=True)
    writervideo = animation.FFMpegWriter(fps=60)
    ani.save(par['path']+'\\simple_car.mp4', writer=writervideo)
    return ani




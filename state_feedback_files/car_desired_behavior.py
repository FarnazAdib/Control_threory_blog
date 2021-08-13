import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
from collections import deque

import os


def simple_car(par):
    # Double Integrator Dynamics
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    Kx = par["Kx"]
    Ky = par["Ky"]
    # integrate your ODE using scipy.integrate

    def derivs(state, t):
        state_x = (state[0: 2]).reshape((2, 1))
        state_y = (state[2: 4]).reshape((2, 1))
        dxdt = (A - B @ Kx) @ state_x
        dydt = (A - B @ Ky) @ state_y
        dstate_dt = np.concatenate([dxdt, dydt], axis=0)
        return dstate_dt.flatten()

    trajectory = integrate.odeint(derivs, par["init_state"], np.arange(0, par['t_stop'], par['dt']))
    return trajectory


def plot_and_save_simple_car(trajectory, par):
    t = np.arange(0, par['t_stop'], par['dt'])  # create a time array from 0..t_stop sampled at 0.02 second steps
    history_len = int(par['t_stop'] / par['dt'])  # how many trajectory points to display

    x1 = trajectory[:, 0]
    y1 = trajectory[:, 2]

    fig, ax = plt.subplots(figsize=(5, 4))
    plt.title(par['title'])
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-5.0, 5.0)
    ax.set_aspect('equal')
    ax.grid()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.annotate('Target', xy=(0, 0), xycoords='data', xytext=(35, 5), textcoords='offset points',
                horizontalalignment='right', verticalalignment='bottom')

    line, = ax.plot(0, 0, '+', ms=15.0, mec='k')
    line, = ax.plot([], 'o-', lw=2, c='r')
    trace, = ax.plot([], ',-', lw=1, c='b')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
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

your_controller = {
    'init_state': np.array([-3.0, 1.0, 2.0, 1.0]),
    'Kx': np.array([[4.0, 5.0]]),
    'Ky': np.array([[4.0, 5.0]]),
    't_stop': 5,  # how many seconds to simulate
    'dt': 0.02,
    'title': 'State feedback controller',
    'path': os.path.dirname(os.path.realpath(__file__))
}
trajectory = simple_car(your_controller)
ani = plot_and_save_simple_car(trajectory, your_controller)


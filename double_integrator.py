from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque
from IPython.display import HTML, Image

A = np.array([[0.0, 1.0], [0.0, 0.0]])
B = np.array([[0.0], [1.0]])
Kx = np.array([[-4.0, -3.0]])
Ky = np.array([[-4.0, -3.0]])
t_stop = 5  # how many seconds to simulate
# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)
history_len = int(t_stop/dt)  # how many trajectory points to display

def derivs(state, t):
    state_x = (state[0: 2]).reshape((2, 1))
    state_y = (state[2: 4]).reshape((2, 1))
    dxdt = (A + B @ Kx) @ state_x
    dydt = (A + B @ Ky) @ state_y
    dstate_dt = np.concatenate([dxdt, dydt], axis=0)
    return dstate_dt.flatten()


px = -3.0
vx = 1.0
py = 2.0
vy = 1.0

# initial state
state = np.array([px, vx, py, vy])

# integrate your ODE using scipy.integrate.
trajectory = integrate.odeint(derivs, state, t)

x1 = trajectory[:, 0]
y1 = trajectory[:, 2]


fig = plt.figure(figsize=(10, 4))
gs = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(gs[:, 0], autoscale_on=False, xlim=(-5.0, 5.0), ylim=(-5.0, 5.0))
ax1.set_aspect('equal')
ax1.grid()
ax1.set_xlabel('x')
ax1.set_ylabel('y')

line, = ax1.plot([], 'o-', lw=2)
trace, = ax1.plot([],',-', lw=1)
time_template = 'time = %.1fs'
time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)
history_x, history_y, history_t = deque(maxlen=history_len), deque(maxlen=history_len), deque(maxlen=history_len)

ax2 = fig.add_subplot(gs[0, 1], autoscale_on=False, xlim=(0.0, t_stop), ylim=(-5.0, 5.0))
line2, = ax2.plot([], 'o-', lw=2)
trace2, = ax2.plot([],',-', lw=1)
ax2.grid()
ax2.set_xlabel('time')
ax2.set_ylabel('x')


ax3 = fig.add_subplot(gs[1, 1], autoscale_on=False, xlim=(0.0, t_stop), ylim=(-5.0, 5.0))
line3, = ax3.plot([], 'o-', lw=2)
trace3, = ax3.plot([],',-', lw=1)
ax3.grid()
ax3.set_xlabel('time')
ax3.set_ylabel('y')


# fig = plt.figure(figsize=(5, 4))
# ax = fig.add_subplot(autoscale_on=False, xlim=(-5.0, 5.0), ylim=(-5.0, 5.0))
# ax.set_aspect('equal')
# ax.grid()
#
# line, = ax.plot([], 'o-', lw=2)
# trace, = ax.plot([],',-', lw=1)
# time_template = 'time = %.1fs'
# time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)

def animate(i):
    thisx = [x1[i]]
    thisy = [y1[i]]
    thist = i*dt

    if i == 0:
        history_x.clear()
        history_y.clear()
        history_t.clear()

    history_x.appendleft(thisx[0])
    history_y.appendleft(thisy[0])
    history_t.appendleft(thist)

    line.set_data(thisx, thisy)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))

    line2.set_data(thist, thisx)
    trace2.set_data(history_t, history_x)

    line3.set_data(thist, thisy)
    trace3.set_data(history_t, history_y)

    return line, trace, time_text, line2, trace2, line3, trace3


ani = animation.FuncAnimation(
    fig, animate, len(trajectory), interval=dt*1000, blit=True)
# ani.save('pen.gif', writer='Pillow', fps=60)
# Image(url='../../pen.gif')


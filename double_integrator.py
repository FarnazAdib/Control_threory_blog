import numpy as np
import scipy.integrate as integrate
from fun_lib import plot_simple_car


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


your_controller = {
    'init_state': np.array([-3.0, 1.0, 2.0, 1.0]),
    'Kx': np.array([[4.0, 5.0]]),
    'Ky': np.array([[4.0, 5.0]]),
    't_stop': 5,  # how many seconds to simulate
    'dt': 0.02,
    'title': 'State feedback controller'
}
trajectory = simple_car(your_controller)
ani = plot_simple_car(trajectory, your_controller)

P_controller = {
    'init_state': np.array([-3.0, 1.0, 2.0, 1.0]),
    'Kx': np.array([[4.0, 0.0]]),
    'Ky': np.array([[4.0, 0.0]]),
    't_stop': 5,  # how many seconds to simulate
    'dt': 0.02,
    'title': 'Output feedback or P controller'
}

trajectory_P = simple_car(P_controller)
ani_P = plot_simple_car(trajectory_P, P_controller)

D_controller = {
    'init_state': np.array([-3.0, 1.0, 2.0, 1.0]),
    'Kx': np.array([[0, 5.0]]),
    'Ky': np.array([[0, 5.0]]),
    't_stop': 5,  # how many seconds to simulate
    'dt': 0.02,
    'title': 'D controller'
}

trajectory_D = simple_car(D_controller)
ani_D = plot_simple_car(trajectory_D, D_controller)

"""Tunnel Navigation Task"""

from rlpy.Domains.Domain import Domain
from TunnelGame.Game import Game
from TunnelGame.GameVis import GameVis
import numpy as np
from itertools import product
from rlpy.Tools import plt
import math
import time




class TunnelDomain(Domain):

    """
    Simulation of balancing a bicycle.

    **STATE:**
    The state of the domain consists of 2 * N rectangles which represent the
    floor and ceiling of the tunnel as well as the agent's properties.

    * ``rectangles:``   the rectangles in the environment.
    * ``heli_y:``       screen height of agent.
    * ``heli_x:``       screen distance of agent
    * ``heli_vy:``       velocity of agent with respect to y

    **ACTIONS:**

    * a in [0, 1]: accelerate on or off

    **REFERENCE:**

    .. seealso::

    .. warning::

    """

    #: only update the graphs in showDomain every x steps
    show_domain_every = 1

    episode_n = 0
    episodeCap = 50000  #: Total episode duration is ``episodeCap * dt`` sec.
    # store samples of current episode for drawing
    episode_data = np.zeros((6, episodeCap + 1))
    dt = 0.01  #: Frequency is ``1 / dt``.

    def __init__(self, vis=None):
        self.game = Game(screen_width=1280, screen_height=1024)
        print('Tunnel Domain __init__')
        # The new Domain MUST set these variables
        # BEFORE calling the superclass __init__() function:
        self.statespace_limits = np.array([[0, 1000000],
                                          [0, 1000000],
                                          [0, 1000000],
                                          [0, 1000000],
                                          [0, 1000000]])
        self.continuous_dims = np.arange(5)
        self.DimNames = ['s0', 's1', 's2', 's3', 's4']
        self.discount_factor = 0.98
        self.actions = self.game.available_actions()
        self.actions_num = len(self.actions)

        if vis is not None:
            self.vis = GameVis(self.game, master=vis)

        super(TunnelDomain, self).__init__()

    def step(self, a):
        # print('tick:{}'.format(self.t))
        self.t += 1
        # action = self.actions[a]
        # update tunnel
        self.game.do_action(a)
        self.game.tick()

        ns = self.game.sensors.last_vals

        s = self.state
        self.state = ns

        self.episode_data[:-1, self.t] = self.state
        self.episode_data[-1, self.t - 1] = a

        return self._reward(s), ns, self.isTerminal(), self.possibleActions()

    def isTerminal(self):
        return self.game.tunnel.is_collision(self.game.heli)

    def _reward(self, s):
        return -1. if self.isTerminal() else 0.

    def possibleActions(self):
        return np.arange(2)

    def s0(self):
        # non-healthy stable state of the system
        # print('Domain _s0 epsode:{}'.format(self.episode_n))
        self.episode_n += 1
        self.game.start_new()
        self.t = 0
        s = np.zeros(5)
        self.state = s
        self.episode_data[:] = np.nan
        self.episode_data[:-1, 0] = s
        # print('{},{}{}'.format(s, self.isTerminal(), self.possibleActions()))
        return s, self.isTerminal(), self.possibleActions()

    def showDomain(self, a=0, s=None):
        """
        shows a live graph of each observable dimension
        """
        print('v ep[{}] tick[{}] {} {}'.format(self.episode_n, self.t, a, s))
        #if self.vis is None:
        #    return

        # self.vis.draw()

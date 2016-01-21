from Tunnel import Tunnel
from Helicopter import Helicopter
from SensorArray import SensorArray
import math
import numpy as np

from empowerment.accumulator import Accumulator

class Game(object):
    def __init__(self,
                 screen_width=1280,
                 screen_height=1024,
                 playable=True,
                 random_state=np.random.RandomState()):
        print('Game __init__')
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.random_state = random_state
        self.start_new()

        self.sensor_array = SensorArray()
        self.accumulators = [Accumulator(2) for s in self.sensor_array.sensors]
        self.diff_accumulators = [Accumulator(2) for s in self.sensor_array.sensors]
        self.last_action = None

    def start_new(self):
        self.tunnel = Tunnel(self.screen_width,
                             self.screen_height,
                             num_rect=40,
                             passage_height=400,
                             random_state=self.random_state)
        self.heli = Helicopter(self.screen_width/40, self.screen_height/2)

    def do_action(self, idx):
        if self.heli is not None:
            self.heli.set_action(self.heli.A[idx])

    def is_terminal(self):
        return self.heli is None or self.tunnel.is_collision(self.heli)

    def available_actions(self):
        return self.heli.A

    def think_about_it(self):
        for idx, a in enumerate(self.accumulators):
            print('sensor[{}]'.format(idx))
            a.emp()
        print('-----dif accumulatrs')
        for idx, a in enumerate(self.diff_accumulators):
            print('sensor[{}]'.format(idx))
            a.emp()


    def tick(self):
        self.tunnel.tick()
        self.heli.tick()

        stuff = self.tunnel.rects if self.tunnel.obstacle is None else self.tunnel.rects + [self.tunnel.obstacle]

        self.sensor_array.sense(self.heli.x_screen,
                                self.heli.y_screen,
                                stuff)

        if self.last_action is not None:
            for idx, val in enumerate(self.sensor_array.last_vals):
                self.accumulators[idx].observe(self.last_action, val)

            for idx, val in enumerate(self.sensor_array.last_change):
                self.diff_accumulators[idx].observe(self.last_action, val)

        # not threadsafe.. bleh
        self.last_sensors = self.sensor_array.last_vals
        self.last_action = self.heli.get_action()

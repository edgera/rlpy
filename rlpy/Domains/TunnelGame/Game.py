from Tunnel import Tunnel
from Helicopter import Helicopter
from SensorArray import SensorArray
import math
import numpy as np
import os

from empowerment.accumulator import Accumulator
from numpy import genfromtxt




class Game(object):
    def __init__(self,
                 screen_width=1280,
                 screen_height=1024,
                 playable=True,
                 random_state=np.random.RandomState(23)):
        print('Game __init__')
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.random_state = random_state
        self.start_new()

        self.sensor_array = SensorArray()
        self.accumulators = [Accumulator(2) for s in self.sensor_array.sensors]
        self.diff_accumulators = [Accumulator(2) for s in self.sensor_array.sensors]
        self.last_action = None

        self.tick = 0





    def start_new(self):
        self.tunnel = Tunnel(self.screen_width,
                             self.screen_height,
                             num_rect=40,
                             passage_height=400,
                             random_state=np.random.RandomState(23))
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
            a.build_emp_map()
        print('-----dif accumulatrs')
        for idx, a in enumerate(self.diff_accumulators):
            print('sensor[{}]'.format(idx))
            a.build_emp_map()



    def sense_stuff(self):
        stuff = self.tunnel.rects if self.tunnel.obstacle is None else self.tunnel.rects + [self.tunnel.obstacle]

        self.sensor_array.sense(self.heli.x_screen,
                                self.heli.y_screen,
                                stuff)

    def log_senses(self):
        emp = []
        if self.last_action is not None:
            with open('action_.log', 'ab') as log:
                log.write('{},'.format(self.last_action))
                for s in self.last_sensors:
                    log.write('{},'.format(s))
                for s in self.last_diff:
                    log.write('{},'.format(s))
                log.write('\n')
            with open('result_.log', 'ab') as log:
                for s in self.sensor_array.last_vals:
                    log.write('{},'.format(s))
                for s in self.sensor_array.last_change:
                    log.write('{},'.format(s))
                log.write('\n')

            for idx, val in enumerate(self.sensor_array.last_vals):
                self.accumulators[idx].observe(self.last_action, val)
                emp.append(self.accumulators[idx].get_emp(val))

            for idx, val in enumerate(self.sensor_array.last_change):
                self.diff_accumulators[idx].observe(self.last_action, val)
                emp.append(self.diff_accumulators[idx].get_emp(val))

        self.last_emp = emp


    def tick(self):
        self.tunnel.tick()
        self.heli.tick()

        self.sense_stuff()
        self.log_emp()

        # not threadsafe.. bleh
        self.last_sensors = self.sensor_array.last_vals
        self.last_diff = self.sensor_array.last_change
        self.last_action = self.heli.get_action()

        if self.is_terminal():
            # add futility of death
            for aidx, a in enumerate(self.heli.A):
                for i in range(100):
                    for idx, val in enumerate(self.sensor_array.last_vals):
                        self.accumulators[idx].observe(aidx, val)

                    for idx, val in enumerate(self.sensor_array.last_change):
                        self.diff_accumulators[idx].observe(aidx, val)








class GameReplay(Game):
    def __init__(self, replay_folder):
        super(Game, self).__init__()
        self.replay_folder = replay_folder

        self.tunnel_csv = genfromtxt(os.path.join(replay_folder, 'tunnel.csv'),
                                     delimiter=',')


    def array_to_rects(self, row):
        rects = []
        for t, b, l, r in zip(*[iter(vars)]*4):
            r = Rect(rect_c.t, rect_c.b, rect_c.r, rect_c.r+self.rect_width)
            rects.append(r)

        return rects

    def tick(self):
        # update tunnel, heli, obs
        rect_row = self.tunnel_csv[self.tick]
        tunnel = self.array_to_rects(rect_row)

        self.tunnel.rects = tunnel

        # self.tunnel.obstacle = []
        # self.heli.y_vel = 0
        # self.heli.x_screen = 0
        # self.heli.y_screen = 0


        # self.sense_stuff()
        # self.log_emp()
        #
        # # not threadsafe.. bleh
        # self.last_sensors = self.sensor_array.last_vals
        # self.last_diff = self.sensor_array.last_change
        # self.last_action = self.heli.get_action()
        #
        # if self.is_terminal():
        #     # add futility of death
        #     for aidx, a in enumerate(self.heli.A):
        #         for i in range(100):
        #             for idx, val in enumerate(self.sensor_array.last_vals):
        #                 self.accumulators[idx].observe(aidx, val)
        #
        #             for idx, val in enumerate(self.sensor_array.last_change):
        #                 self.diff_accumulators[idx].observe(aidx, val)
        #
        #
        #
        #

        self.tick += 1

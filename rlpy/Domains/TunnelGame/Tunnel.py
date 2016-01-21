import numpy as np
import math
from Rect import Rect


def is_rect_overlap(a, b):
    if a.b < b.t:
        pass
    elif a.t > b.b:
        pass
    elif a.l > b.r:
        pass
    elif a.r < b.l:
        pass
    else:
        return True

    return False


class Tunnel(object):
    def __init__(self, screen_width, screen_height, num_rect, passage_height,
                 random_state):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.random_state = random_state
        # num rect is the measure of how many fit accross the screen
        # there will really be 2*(num_rect + 1) rects total for ceil and floor
        self.rect_num = num_rect
        self.rect_width = screen_width / num_rect
        # set the distance between two obstacles.
        self.obstacle_offset = screen_width / 10
        self.obstacle_width = 50
        self.obstacle_height = 150
        self.obstacle = None
        self.path_momentum_p = .05
        self.path_momentum_sign = 1
        self.path_momentum_max = 10

        self.screen_advance_distance = 11

        self.rects = []
        assert(screen_height > passage_height)
        # top
        self.rects.append(Rect(0,
                          (screen_height-passage_height)/2,
                          0,
                          self.rect_width))
        # bot
        self.rects.append(Rect((screen_height+passage_height)/2,
                          screen_height,
                          0,
                          self.rect_width))

        # create a 'smooth' tunnel. we already have the first rects
        for i in range(num_rect):
            self.rects += self.next_rects(self.rects[-2], self.rects[-1])

    def next_rects(self, rect_c, rect_f):
        if self.random_state.uniform(0, 1) < self.path_momentum_p:
            self.path_momentum_sign *= -1

        increment = self.path_momentum_sign * \
            math.floor(self.path_momentum_max * self.random_state.uniform(0, 1))
        rect_c2 = Rect(rect_c.t, rect_c.b, rect_c.r, rect_c.r+self.rect_width)
        rect_f2 = Rect(rect_f.t, rect_f.b, rect_f.r, rect_f.r+self.rect_width)
        if rect_c.b+increment > 0 and rect_f.t+increment < self.screen_height:
            rect_c2.b += increment
            rect_f2.t += increment

        return [rect_c2, rect_f2]

    def tick(self):
        for rect in self.rects:
            rect.l -= self.screen_advance_distance
            rect.r -= self.screen_advance_distance

        if self.obstacle is not None:
            self.obstacle .l -= self.screen_advance_distance
            self.obstacle .r -= self.screen_advance_distance

        if self.rects[0].r < 0:
            del self.rects[0]
            del self.rects[0]
            self.rects += self.next_rects(self.rects[-2], self.rects[-1])

            # do new obstacle
            if self.obstacle is None or self.obstacle.r < 0:
                center = (self.rects[-1].t + self.rects[-2].b)/2
                self.obstacle = Rect(center-self.obstacle_height/2,
                                     center+self.obstacle_height/2,
                                     self.screen_width,
                                     self.screen_width + self.obstacle_width)

    def is_collision(self, heli):

        possible_width = int(math.ceil(heli.width/self.rect_width)+1)
        index_first = int((2*math.floor(heli.x_screen/self.rect_width))+1)
        a = Rect(heli.y_screen,
                 heli.y_screen+heli.height,
                 heli.x_screen,
                 heli.x_screen+heli.width)

        for i in range(index_first,
                       index_first + 2*possible_width):
            if is_rect_overlap(a, self.rects[i]):
                return True

        # also check the obstacle
        if self.obstacle is not None and is_rect_overlap(a, self.obstacle):
            return True

        return False

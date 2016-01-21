import math
# Returns 1 if the lines intersect, otherwise 0. In addition, if the lines
# intersect the intersection point may be stored in the floats i_x and i_y.
def get_line_intersection(p0_x, p0_y, p1_x, p1_y,
                          p2_x, p2_y, p3_x, p3_y):
    s1_x = p1_x - p0_x
    s1_y = p1_y - p0_y
    s2_x = p3_x - p2_x
    s2_y = p3_y - p2_y

    if s1_x != 0 and s2_x != 0 and math.fabs(s1_y/s1_x - s2_y/s2_x) < .0000001:
        return (None, None)

    try:
        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) /\
            (-s2_x * s1_y + s1_x * s2_y)
        t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) /\
            (-s2_x * s1_y + s1_x * s2_y)
    except:
        print("Broken points {},{} {},{}".format(s1_x, s1_y, s2_x, s2_y))
        return (None, None)

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        # Collision detected
        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)
        return (i_x, i_y)

    return (None, None)

class SensorArray(object):
    def __init__(self):
        self.sensors = [(2000, 2000),
                        (2000, 0),
                        (2000, -2000),
                        (2000, 1000),
                        (2000, -1000)]
        self.last_vals = [0,0,0,0,0]
        self.last_change = [0,0,0,0,0]
        self.last_impacts = [(0,0),(0,0),(0,0),(0,0),(0,0)]

    def sense(self, s_x, s_y, rects):
        '''
        tunnel locations are wrt the screen.
        x, y are where the sensor origin is wrt the screen.
        '''
        sensor_values = []
        impacts = []
        for idx, sensor in enumerate(self.sensors):
            min_sq_dist = 1000000
            (min_x, min_y) = (1000, 1000)

            for rect in rects:
                sides = [(rect.l,rect.t,rect.r,rect.t),
                         (rect.l,rect.b,rect.r,rect.b),
                         (rect.l,rect.t,rect.l,rect.b)]
                for side in sides:
                    (x, y) = get_line_intersection(s_x,
                                                   s_y,
                                                   s_x+sensor[0],
                                                   s_y+sensor[1],
                                                   side[0],
                                                   side[1],
                                                   side[2],
                                                   side[3]
                                                   )
                    if x is not None:
                        sq_dist = (s_x-x)*(s_x-x)\
                                  + (s_y-y)*(s_y-y)

                        (min_x,min_y) = (x,y) if sq_dist<min_sq_dist else (min_x,min_y)
                        min_sq_dist = sq_dist if sq_dist<min_sq_dist else min_sq_dist
            sensor_values.append(min_sq_dist)
            impacts.append((min_x,min_y))
            #
        self.last_impacts = impacts
        for idx, val in enumerate(self.last_vals):
            self.last_change[idx] = sensor_values[idx]-val

        self.last_vals = sensor_values
        return sensor_values, impacts


class Helicopter(object):
    def __init__(self, x, y):
        self.y_vel = 0
        self.x_screen = x
        self.y_screen = y

        #
        self.width = 70
        self.height = 50

        self.A = [self.a1, self.a2]
        self.current_action = self.a1

    def set_action(self, action):
        self.current_action = action

    def get_action(self):
        '''
        returns idx of self.current_action
        '''
        return self.A.index(self.current_action)

    def tick(self):
        # TODO check if crashed?

        # do Action
        self.current_action()

        # dynamics
        self.y_screen += self.y_vel

    def a1(self):
        """
        increase y_vel by .25 (gravity)
        """
        self.y_vel += .25

    def a2(self):
        """
        decrease y_vel by .25
        """
        self.y_vel += -.25

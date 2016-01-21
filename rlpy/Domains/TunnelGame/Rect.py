
class Rect(object):
    """
    a screen rectangle.
    """
    def __init__(self, top=0, bot=0, left=0, right=0):
        # top is WRT the screen. eg, the top should have a lower value
        # than bot, if the top left corner is origin.
        self.t = top
        self.b = bot
        self.l = left
        self.r = right

    def __str__(self):
        return "{} {} {} {}".format(self.t, self.b, self.l, self.r)

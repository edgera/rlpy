from Game import Game
from Tkinter import *
from SensorArray import SensorArray

class GameVis(object):
    def __init__(self, game, master=None):
        # master is Tk()

        self.w = Canvas(master,
                        width=game.screen_width,
                        height=game.screen_height)
        self.w.focus_set()
        self.w.pack()
        self.w.bind("<Button-1>", self.callback_click)
        self.w.bind("<ButtonRelease-1>", self.callback_release)
        self.w.bind("<Key>", self.cb_start_new)

        self.screen_width = game.screen_width
        self.screen_height = game.screen_height

        self.game = game
        self.running = False



    def cb_start_new(self, event):
        print("starting new game")
        self.game.start_new()
        if not self.running:
            self.running = True
            self.schedule_tick()

    def callback_release(self, event):
        # print "releaseed at", event.x, event.y
        if self.game is not None:
            self.game.do_action(0)

    def callback_click(self, event):
        # print "clicked at", event.x, event.y
        if self.game is not None:
            self.game.do_action(1)

    def draw(self):
        self.w.delete("all")

        rects = self.game.tunnel.rects
        for rect in rects:
            self.w.create_rectangle((rect.l,
                                     rect.t,
                                     rect.r,
                                     rect.b), fill='green', width=0)
        obs = self.game.tunnel.obstacle
        if obs is not None:
            self.w.create_rectangle((obs.l,
                                     obs.t,
                                     obs.r,
                                     obs.b), fill='grey')


        heli = self.game.heli
        self.w.create_rectangle(heli.x_screen,
                                heli.y_screen,
                                heli.x_screen+heli.width,
                                heli.y_screen+heli.height)

        stuff = rects if obs is None else rects + [obs]
        # sensor lines
        impacts = self.game.sensor_array.last_impacts

        emp = self.game.last_emp

        for idx, sensor in enumerate(self.game.sensor_array.sensors):
            try:
                self.w.create_line(heli.x_screen,
                                    heli.y_screen,
                                    heli.x_screen+sensor[0],
                                    heli.y_screen+sensor[1],
                                    width=int((emp[idx]/sum(emp))*100))

                self.w.create_rectangle(impacts[idx][0],
                                    impacts[idx][1],
                                    impacts[idx][0]+4,
                                    impacts[idx][1]+4, fill='red')
            except:
                pass

        print("sensors: {}".format(self.game.sensor_array.last_vals))



    def schedule_tick(self):
        self.game.tick()
        self.draw()

        if not self.game.is_terminal():
            self.w.after(20, self.schedule_tick)
        else:
            self.running = False
            # self.game.think_about_it()

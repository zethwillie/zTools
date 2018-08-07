from functools import partial
import maya.cmds as cmds

class Window(object):
    """create a basic window with room to put more stuff, stuff goes into either common or custom UI methods"""

    def __init__(self, name="Test Window", w=420, h=200):
        ####### modify for inheritence ########
        self.windowName = name
        self.windowSize = [w, h]
        self.sizeable = True

        self.create_UI()

    def create_UI(self):
        """creates the UI """

        self.winWidth = self.windowSize[0]
        height = self.windowSize[1]

        if (cmds.window("zbw_win", exists=True)):
            cmds.deleteUI("zbw_win")

        self.window = cmds.window("zbw_win", title=self.windowName, w=self.winWidth, h=height, s=self.sizeable)

        #menus for future
        self.menus()

        cmds.setParent(self.window)
        self.formLO = cmds.formLayout(nd=100, w=self.winWidth)
        # self.widgets["topColumnLO"] = cmds.columnLayout(w=self.winWidth)
        self.scrollLO = cmds.scrollLayout(vst=10)
        self.lowColumnLO = cmds.columnLayout(w=self.winWidth)
        cmds.formLayout(self.formLO, e=True, attachForm = [(self.scrollLO, "top", 0), (self.scrollLO, "left", 0), (self.scrollLO, 'right', 0), (self.scrollLO, 'bottom', 35)])

        self.common_UI()
        
        self.custom_UI()

        self.buttons_UI()

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, w=self.winWidth, h=height)


    def common_UI(self):
        #########  modify for inheritence ###########
        cmds.text('this is where the common UI elements go')
        cmds.separator(h=100)


    def custom_UI(self):
        #########  modify for inheritence ###########
        cmds.text("this is where the custom UI elements go")
        cmds.separator(h=200)


    def buttons_UI(self):
        #########  modify for inheritence ###########
        butWidth = self.winWidth/3 - 10

        self.applyCloseBut = cmds.button(w=butWidth, h=30, l='Apply and Close', p=self.formLO, bgc=(.5, .7, .5), c=partial(self.action, 1))
        self.applyBut = cmds.button(w=butWidth, h= 30, l='Apply', p=self.formLO, bgc=(.7, .7, .5), c=partial(self.action, 0))
        self.closeBut = cmds.button(w=butWidth, h=30, l="Close Window", p=self.formLO, bgc=(.7, .5, .5), c=self.close_window)

        cmds.formLayout(self.formLO, e=True, attachForm=[(self.applyCloseBut, 'bottom', 5), (self.applyCloseBut, 'left', 5)])
        cmds.formLayout(self.formLO, e=True, attachForm=[(self.closeBut, 'bottom', 5), (self.closeBut, 'right', 5)])
        cmds.formLayout(self.formLO, e=True, attachForm=[(self.applyBut, 'bottom', 5)])
        cmds.formLayout(self.formLO, e=True, attachControl=[(self.applyBut, 'left', 5, self.applyCloseBut),(self.applyBut, 'right', 5, self.closeBut)])


    def action(self, close, *args):
        ############ modify for inheritence #############
        #do the action here

        #close window
        if close:
            self.close_window()


    def close_window(self, *args):
        cmds.deleteUI(self.window)


    def menus(self):
        #########  modify for inheritence ###########
        #self.widgets["testMenu"] = cmds.menu(l="test")
        self.menuMB = cmds.menuBarLayout()
        self.fileMenu = cmds.menu(label="file")
        cmds.menuItem(l='reset values', c=self.reset_values)
        cmds.menuItem(l="save values", c=self.save_values)
        cmds.menuItem(l="load values", c=self.load_values)
        self.helpMenu = cmds.menu(l="help")
        cmds.menuItem(l="print help", c=self.print_help)


    def print_help(self, *args):
        #########  modify for inheritence ###########
        print("test help")

    def reset_values(self, *args):
        #########  modify for inheritence ###########
        print("test values reset")


    def save_values(self, *args):
        #########  modify for inheritence ###########
        print("test save values")


    def load_values(self, *args):
        #########  modify for inheritence ###########
        print("test load values")
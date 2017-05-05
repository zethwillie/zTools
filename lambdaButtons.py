# PURE
io = lambda f: lambda _: f() # dismiss, e.g., a useless arg in a UI call
doboth = lambda f: lambda g: lambda: [f(),g()]

# IMPURE
ball = lambda: cmds.polySphere(name="aBall")[0]
kill = lambda: cmds.delete("aBall")

# abstracted-out enable-state handlers (for all controls)
enable = lambda ui: lambda: cmds.control(ui, edit=True, enable=True)
disable = lambda ui: lambda: cmds.control(ui, edit=True, enable=False)

# example
cmds.window()
cmds.showWindow()
cmds.columnLayout()
ballbtn = cmds.button("make a ball")
noballbtn = cmds.button("destroy a ball", enable=False)

# compose UI state handling with function calls
cmds.button(ballbtn, edit=True, command=io(doboth(ball)(enable(noballbtn))))
cmds.button(noballbtn, edit=True, command=io(doboth(kill)(disable(noballbtn))))

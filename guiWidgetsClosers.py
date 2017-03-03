gui widget closures

def self_aware_buttons():
    
    
    def cogito( label):
        btn = cmds.button(label = label)
        
        def handler(*_):
            print "hello, I'm a button named", btn, "amd my label is", cmds.button(btn, q=True, l=True) 
        
        cmds.button(btn, e=True, c=handler)
        return btn
        
    w = cmds.window(title= 'the window')
    c = cmds.columnLayout()
    b = cogito("a button")
    c = cogito("a button")
    d = cogito("another button")
    cmds.showWindow(w)
        
self_aware_buttons()
# Python code
import maya.cmds as mc

#TO-DO----------------figure out how to just add a new menu item to the EXISTING menu set (like stick it in as index 0 of the menu set rather than deleting the menu set)


# The name to give our custom, context-sensitive, Alt+RMB popupMenu:
POP_NAME = 'myCustomPopupMenu'

def overrideDagMenuProc():
    """
    This function will override the RMB-menu created by dagMenuProc().
    It returns the name of the object Alt+RMB'd on:
    """
    # This creates a new menu, for the object Alt+RMB'd on, populated with the
    # guts of what dagMenuProc() would normally build:
    mc.dagObjectHit(menu=POP_NAME)
    # Get a list of all the children in that menu:
    popChildren = mc.popupMenu(POP_NAME, query=True, itemArray=True)
    # The menu item's name is the leaf name of the node:  If there are duplicate
    # names in the scene, this is always the leaf.  To get the full path, we
    # need to query the select command embedded in the menuItem:
    command = mc.menuItem(popChildren[0], query=True, command=True)
    fullName = command.split(' ')[-1]
    # Now delete the menu items created by dagMenuProc(), giving us an empty menu:

# TODO----------this is the line of code. . . maybe append my script onto the top of the list of children??
    mc.popupMenu(POP_NAME, edit=True, deleteAllItems=True)

    # Finally return the name of our node, which will be used by postMenuCommand
    # to build the top label in the empty menu:
    return fullName

def postMenuCommand(*args):
    """
    This function is passed to, and executed by the menu created via makePopup()
    whenever the popupMenu is shown.  It's what you'd update to have custom menu
    items appear based on what's selected.
    """
    # Delete all the items from any pre-existing menus:
    if mc.popupMenu(POP_NAME, exists=True):
        mc.popupMenu(POP_NAME, edit=True, deleteAllItems=True)

    # Make our menu the current menu for any new children:
    mc.setParent(POP_NAME, menu=True)
    if mc.dagObjectHit():  # undocumented command!
        # If the user has Alt+RMB'd over a node, capture the return of the
        # function that overrides the dagMenuProc's popupMenu.  The return is
        # the full name of the node that has been Alt+RMB'd over... and use it as
        # the label for the menu.  Extract the leaf name from the full path:
        fullObjectName = eval('overrideDagMenuProc()')
        leafObjectName = fullObjectName.split("|")[-1]
        mc.menuItem(label=leafObjectName)

        # Here, any custom code can be authored that is based on the object name
        # For example, track if there are any highlighted components:
        componentPreSelect = mc.ls(preSelectHilite=True)

        if len(componentPreSelect):
            mc.menuItem(divider=True)
            mc.menuItem(label=componentPreSelect[0])
    else:
        # Otherwise, no thing Alt+RMB'd on:
        mc.menuItem(label="No object under cursor")

def makePopup():
    """
    Will create the custom, context-sensitive, popupMenu displayed by Alt+RMB'ing
    on a node.
    """
    # Delete the popupMenu if it already exists:
    if mc.popupMenu(POP_NAME, exists=True):
        mc.deleteUI(POP_NAME)

    # Build the popupMenu, envoking a postMenuCommand when it is shown:
    mc.popupMenu(POP_NAME,
                 button=3,
                 #TO-DO----------------altModifier. . . turn on/off??
                 altModifier=True,
                 markingMenu=True,
                 parent='viewPanes',
                 postMenuCommand=postMenuCommand)


makePopup()
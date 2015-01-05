#!/usr/bin/env python

from gi.repository import Gtk, Vte, GObject
from gi.repository import GLib
import os

from splitpane import SplitPane

class Terminal(Vte.Terminal):

    def __init__(self, parent):
        super(Terminal, self).__init__()

        self.parent = parent

        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None)
      
    """
    Returns a new SplitPane, whos first child is the current terminal, and second child is a new terminal
    """   
            
    def split(self, orientation):
        size = self.get_allocation().width if orientation == Gtk.Orientation.HORIZONTAL else self.get_allocation().height;

        split_pane = SplitPane(self.parent)
        split_pane.set_orientation(orientation)

        if (isinstance(self.parent, SplitPane)):
            self.parent.replace(self, split_pane);

        # Put current terminal into split pane
        split_pane.add1(self)
        self.parent = split_pane
        
        # Put new terminal into split pane
        new_terminal = Terminal(split_pane)
        split_pane.add2(new_terminal)
        new_terminal.parent = split_pane
        

        split_pane.divide_in_half(size)

        return (split_pane, new_terminal)
        
    """
    Destroy the current terminal, returning the terminal which should now be active
    """    
    def close(self):
        if (isinstance(self.parent, SplitPane)):
            other_child = self.parent.get_other_child(self)
            
            self.parent.remove(self)
            self.parent.remove(other_child)
            
            if (isinstance(self.parent.parent, SplitPane)):
                self.parent.parent.replace(self.parent, other_child);

        self.destroy()


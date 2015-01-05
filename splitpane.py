#!/usr/bin/env python

from gi.repository import Gtk, Vte, GObject
from gi.repository import GLib
import os

class SplitPane(Gtk.Paned):

    def __init__(self, parent):
        super(SplitPane, self).__init__()
        self.parent = parent
    
    def replace(self, child, new_child):
        if (self.get_child1() == child):
            self.remove(child)
            self.add1(new_child)
        elif (self.get_child2() == child):
            self.remove(child)
            self.add2(new_child)  
            
    def divide_in_half(self, size):
        # Split the pane 'in half'
        self.set_position(size/2)
        self.show_all()

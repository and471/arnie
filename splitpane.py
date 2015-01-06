#!/usr/bin/env python

from gi.repository import Gtk, Vte, GObject
from gi.repository import GLib
import os

import terminal

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
        new_child.parent = self
            
    def divide_in_half(self, size):
        # Split the pane 'in half'
        self.set_position(size/2)
        self.show_all()
        
    def get_other_child(self, child):
        if (self.get_child1() == child):
            return self.get_child2()
        elif (self.get_child2() == child):
            return self.get_child1()
            
    def get_nearest_terminal(self):
        if (self.get_child1() == None and self.get_child2() == None):
            return None
            
        if (isinstance(self.get_child1(), terminal.Terminal)):
            return self.get_child1()
        if (isinstance(self.get_child2(), terminal.Terminal)):
            return self.get_child2()
            
        if (self.get_child1().get_nearest_terminal() != None):
            return self.get_child1().get_nearest_terminal()
        return self.get_child2().get_nearest_terminal()

        
class SinglePane(Gtk.Alignment):

    def __init__(self):
        super(SinglePane, self).__init__()
    
    def add1(self, widget):
        self.add(widget)
        
    def add2(self, widget):
        self.add(widget)
    
    def get_child(self):
        return self.get_children()[0]
    
    def replace(self, child, new_child):
        self.remove(child)
        self.add(new_child) 
        
        new_child.parent = self
            
    def divide_in_half(self, size):
        pass
        
    def get_other_child(self, child):
        return None
        
    def get_nearest_terminal(self):
        return None

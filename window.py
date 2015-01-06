#!/usr/bin/env python

from gi.repository import Gtk, Vte, GObject
from gi.repository import GLib
import os

from terminal import Terminal
from splitpane import SplitPane, SinglePane

class Window(Gtk.Window, GObject.GObject):
    __gsignals__ = {
        #"active-terminal-changed": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super(Window, self).__init__()
        self._create_headerbar()
        
        self.connect('delete-event', Gtk.main_quit)
        
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True);
        
        self.active_terminal = None
        self.window_title_changed_signal = None
        self.toplevel = None
        
        self._add_terminal(None, None)
        
        self.show_all()

    def _create_headerbar(self):
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        
        # Horizontal split button
        button_split_horizontal = Gtk.Button()
        button_split_horizontal.add(Gtk.Image.new_from_file("split-horizontal.png"))
        button_split_horizontal.connect("clicked", self._on_button_split_horizontal_clicked)
        
        # Vertical split button
        button_split_vertical = Gtk.Button()
        button_split_vertical.add(Gtk.Image.new_from_file("split-vertical.png"))
        button_split_vertical.connect("clicked", self._on_button_split_vertical_clicked)
        
        # Close terminal button
        button_close = Gtk.Button()
        button_close.add(Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.SMALL_TOOLBAR))
        button_close.connect("clicked", self._on_button_close_clicked)
        
        self.header.pack_start(button_split_horizontal)
        self.header.pack_start(button_split_vertical)
        self.header.pack_start(button_close)
        
        self.header.set_title("Terminal")
        self.set_titlebar(self.header)
        
    def _on_button_split_horizontal_clicked(self, widget):
        if (self.active_terminal == None):
            return
            
        self._add_terminal(self.active_terminal, Gtk.Orientation.HORIZONTAL)
        
    def _on_button_split_vertical_clicked(self, widget):
        if (self.active_terminal == None):
            return
            
        self._add_terminal(self.active_terminal, Gtk.Orientation.VERTICAL)
    
    """
    Destroys the active terminal and focuses the 'next' in line
    """
    def _on_button_close_clicked(self, widget):
        if (self.active_terminal == None):
            return
            
        if (self.active_terminal == self.pane.get_child()):
            Gtk.main_quit()
            return
        
        self._set_active_terminal(self.active_terminal.close())
        
    """
    Creates, packs, focuses and returns a new terminal
    """ 
    def _add_terminal(self, to_split, orientation):
        new_terminal = None
    
        if to_split == None:
            # If there are no terminals
            new_terminal = Terminal(self)
            self.pane = SinglePane()
            new_terminal.parent = self.pane
            self.pane.add(new_terminal)
            self.add(self.pane)
            self._set_active_terminal(new_terminal)
        else:
            # Otherwise create one by splitting
            new_terminal = to_split.split(orientation)
                
        
        new_terminal.connect("focus-in-event", self._on_terminal_focused)
        new_terminal.show()
        new_terminal.grab_focus()

        return new_terminal
    
    """
    Sets the active terminal and handles signals associated with the working directory changing
    """
    def _set_active_terminal(self, terminal):
        # Remove signals from previous active terminal
        if not (self.window_title_changed_signal is None):
            self.active_terminal.disconnect(self.window_changed_signal)
            self.window_title_changed_signal = None
    
        self.active_terminal = terminal;
         
        if (terminal == None):
            return

        # Change window subtitle when directory changes
        self.window_changed_signal = self.active_terminal.connect("window-title-changed",
            self._on_active_terminal_title_changed)
        self._on_active_terminal_title_changed(None)
        
        self.active_terminal.grab_focus()
        
    """
    Sets the headerbar's subtitle and window's title to be the working directory of the active terminal
    """    
    def _on_active_terminal_title_changed(self, widget):
        title = self.active_terminal.get_window_title()
        if not title is None:
            self.header.set_subtitle(title)
        
    def _on_terminal_focused(self, terminal, event):
        self._set_active_terminal(terminal)
    
    
win = Window()
Gtk.main()

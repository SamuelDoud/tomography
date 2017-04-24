"""A user interface for interacting with the network."""

from tkinter import Tk, Frame, Button, Label, Entry, Menu, messagebox, Toplevel

from tomography import Tomography
from Node import Node, Server, EndUser
from Connection import Connection
from Link import Link

class Display(Frame):
    """Provide the user with a visualization of the network and a way to interact with it."""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Tomography")
        self.master.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.tomography = Tomography()
        self.menu_creation()

    def menu_creation(self):
        """
        Helper method to define the menu bar
        """
        self.menu_bar = Menu(self.master)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.edit_menu_create()
        self.file_menu_create()
        self.help_menu_create()
        self.master.config(menu=self.menu_bar)

    def edit_menu_create(self):
        self.edit_menu.add_command(label="Node", command=self.node_popup)
        self.edit_menu.add_command(label="Link", command=self.link_popup)
        self.edit_menu.add_command(label="Connection", command=self.connection_popup)
        self.edit_menu.add_separator
        #self.edit_menu.add_command(label="Remove First", command=self.remove_first)
        #self.edit_menu.add_command(label="Remove Last", command=self.remove_last)
        self.edit_menu.add_command(label="Remove All", command=self.master_blaster)

    def master_blaster(self):
        """Deletes all objects on the graph."""
        #pass an empty list
        self.tomography.connections = []
        self.tomography.nodes = []

    def help_menu_create(self):
        self.help_menu.add_command(label="View Help", command=self.help_message_box)
    
    def help_message_box(self):
        #pause the animation
        self.help_message_str = "Sam Doud needs to write this up"
        #launch the message box
        messagebox.showinfo("Help", self.help_message_str)

    def file_menu_create(self):
        #self.file_menu.add_command(label="Save", command=self.save)
        #self.file_menu.add_command(label="Open", command=self.open)
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        #self.file_menu.add_separator()
        #self.file_menu.add_command(label="Save as GIF", command=self.save_gif_handler)
        #self.file_menu.add_command(label="Save as Video", command=self.save_video_handler)

    
    def node_popup(self):
        self.width = 5
        self.top = Toplevel(self.master)
        self.master.wait_window(self.top)
        self.type_label = Label(self.top, text="Select a node type")
        self.type_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.create_node_submit = Button(self.top, text="Create Node", command=self.node_cleanup)
        self.top.bind("<Return>", self.node_cleanup)

    def node_cleanup(self):
        if self.type_entry.get():
            type_of_node = self.type_entry.get()
            if type_of_node.lower is 'server':
                new_node = Server()
            if type_of_node.lower is 'enduser':
                new_node = EndUser()
            if new_node:
                self.add_node(new_node)
        self.top.destroy()

    def link_popup(self):
        self.width = 5
        self.default_lag = 1
        self.default_buffer = 1
        self.top = Toplevel(self.master)
        self.master.wait_window(self.top)
        self.connection_label = Label(self.top, text="Select a Connection to add a link to")
        self.connection_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.lag_label = Label(self.top, text="Select a lag time")
        self.lag_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.buffer_label = Label(self.top, text="Select a buffer size")
        self.buffer_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.create_node_submit = Button(self.top, text="Create link", command=self.link_cleanup)
        self.top.bind("<Return>", self.node_cleanup)

    def link_cleanup(self):
        if self.connection_entry.get():
            #get the connection. dummy code for now
            c = Connection(1, 2)
            link = Link(c.start_node, c.end_node,
                        self.lag_entry.get()
                        if self.lag_entry.get()
                        else self.default_lag,
                        self.buffer_entry.get()
                        if self.buffer_entry.get()
                        else self.default_buffer)
            self.tomography.connections[self.tomography.connections.index(c)].add_link(link=link)
        self.top.destroy()

    def connection_popup(self):
        self.width = 5
        self.top = Toplevel(self.master)
        self.master.wait_window(self.top)
        if len(self.tomography.nodes) < 2:
            #message that a connection cannot be made
            self.top.destroy()
        self.start_label = Label(self.top, text="Select a start node")
        self.start_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.end_label = Label(self.top, text="Select a end node")
        self.end_entry = Entry(self.top, width=self.width, bd=self.bd)
        self.create_node_submit = Button(self.top, text="Create Node", command=self.node_cleanup)
        self.top.bind("<Return>", self.node_cleanup)

    def connection_cleanup(self):
        if self.start_entry.get() and self.end_entry.get():
            pass
        self.top.destroy()

    def tick(self, time=1):
        """Increment n units of time."""
        if time < 1:
            raise Exception("Must provide a positive real value for time" +
                            "(Although it really should be an integer you oaf.)")
        for _counter in range(time):
            self.tomography.tick()
        self.draw()

    def shutdown(self):
        """Closes the application 'gracefully'."""
        self.master.quit()
        self.master.destroy()

    def add_node(self, node):
        """Add a node to the Tomography.
        The Tomography will assign an address if needed."""
        self.tomography.add_node(node)

    def remove_node(self, node):
        """Safely remove a node from the Tomography."""
        self.tomography.remove_node(node)

    def connect_nodes(self, start_node, end_node):
        """Connect two Nodes. A start node should be upstream of the end_node.ß"""
        self.tomography.add_connection(start_node, end_node)

    def draw(self):
        """Draw all nodes and their connections (along with any notation about data flows)."""
        pass

ROOT = Tk()
WINDOW = Display(master=ROOT)
WINDOW.mainloop()

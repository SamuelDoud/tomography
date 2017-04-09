"""A user interface for interacting with the network."""

from tkinter import Tk, Frame

from tomography import Tomography

class Display(Frame):
    """Provide the user with a visualization of the network and a way to interact with it."""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Tomography")
        self.master.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.tomography = Tomography()

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

import Packet
import Connection
import Node
import Tomography
import Link
import sys
import traceback


def parse(text):
    text = text.lower()
    arguments = text.split(' ')
    # print(text)
    # for argument in arguments:
    #    print(argument)
    if arguments[0] == 'connect':
        print('Attempting to add a node to the network')
        connected_node_address = arguments[1]
        connected_node = None
        weight = arguments[2]
        for node in tomo.nodes:
            if node.address == connected_node_address:
                connected_node = node
        if not connected_node:
            print("Bad address")
            return
        unconnected_node = Node.Node()
        connect_nodes(unconnected_node, connected_node, weight)

    if arguments[0] == 'ping_run':
        ticks = int(arguments[1])
        for _tick in range(ticks):
            tomo.random_pings()
        print(tomo.ping_info())

    if arguments[0] == 'list':
        message = 'Nodes: '
        for node in tomo.nodes[:-1]:
            message += node.address + ', '
        message += tomo.nodes[-1].address + '.'
        print(message)


def connect_nodes(unconnected_node, connected_node, weight):
    """Connects a new node to the network at a given point"""
    weight = int(weight)
    new_connection = Connection.Connection(connected_node, unconnected_node)
    outbound_link = Link.Link(connected_node, unconnected_node, weight)
    inbound_link = Link.Link(unconnected_node, connected_node, weight)
    new_connection.add_link(link=outbound_link)
    new_connection.add_link(link=inbound_link)
    connected_node.add_connection(new_connection, False)
    unconnected_node.add_connection(new_connection, True)
    tomo.add_node(unconnected_node)
    tomo.connections.append(new_connection)
    print('Added ' + unconnected_node.address +
          ' to the model with weight ' + str(weight) + '.')


tomo = Tomography.Tomography()
base_node = Node.Node()
base_node.address = '1'
base_node.address_split = ['1']
tomo.add_node(base_node)
command = None
parse('connect 1 2')
parse('connect 1 2')
parse('connect 1 2')
parse('connect 1 2')
parse('connect 1 2')
parse('connect 1.1 3')
parse('connect 1.2 2')
parse('connect 1.1.1 1')
parse('connect 1.4 2')
parse('connect 1.4 4')
parse('ping_run 20')
while not command:
    try:
        command = str(input("Enter: "))
        parse(command)
    except:
        print('Invalid Syntax from Prompt')
        traceback.print_exc()
    if command.lower() is not 'exit':
        command = None

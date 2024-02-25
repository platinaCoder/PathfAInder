def make_connection(weight, transform_fn=lambda x: x):
    """Creates a connection with a given weight and an optional transformation function."""
    def connection(input_value):
        return transform_fn(input_value * weight)
    return connection

def make_node(node_id, network_state, peering_criteria):
    """Creates a node with peering decision logic.
    
    Args:
        node_id: Unique identifier for the node.
        network_state: Shared state of the network, containing information about all nodes.
        peering_criteria: Function to evaluate and select peers based on specific criteria.
    """
    def node(input_value):
        # Evaluate potential peers from the network state
        potential_peers = peering_criteria(network_state, node_id)
        
        # For demonstration, let's say the node simply communicates with its selected peers
        outputs = []
        for peer_id in potential_peers:
            peer_node = network_state[peer_id]['node']
            output = peer_node(input_value)  # This would be more complex in a real scenario
            outputs.append(output)
        
        # Node's output could be based on its own logic, here simply summing outputs from peers
        return sum(outputs)
    
    # Initial connections could be empty or based on initial peering logic
    initial_peers = peering_criteria(network_state, node_id)
    
    return node, initial_peers

def create_network(num_nodes):
    """Creates a network with a specified number of nodes."""
    network = []
    for _ in range(num_nodes):
        node, connections = make_node()  # Initially, nodes have no connections
        network.append({'node': node, 'connections': connections})
    return network

def add_connection(node, target_node, weight=1.0, transform_fn=lambda x: x):
    """Adds a connection from one node to another with a specified weight and transformation function."""
    connection = make_connection(weight, transform_fn)
    node['connections'].append(connection)
    return connection

def scale_network(network, new_nodes, new_connections):
    """Scales the network by adding new nodes and connections."""
    # Add new nodes
    for _ in range(new_nodes):
        node, connections = make_node()
        network.append({'node': node, 'connections': connections})
    
    # Example logic for adding new connections; specific logic will depend on the network structure
    for i in range(min(len(network), new_connections)):
        add_connection(network[i], network[(i+1) % len(network)], weight=1.2)  # Circular connections for example

    return network

def peering_criteria(network_state, node_id):
    """Example peering criteria function that selects peers based on some criteria.
    
    For simplicity, this example selects peers randomly.
    """
    import random
    potential_peers = [nid for nid in network_state if nid != node_id]  # Exclude self
    selected_peers = random.sample(potential_peers, k=min(2, len(potential_peers)))  # Select up to 2 peers, for example
    return selected_peers

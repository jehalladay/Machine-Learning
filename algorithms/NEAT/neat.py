import numpy as np

print(np.__version__ == '1.20.2')

__version__ = '0.0.1'
__author__ = 'James E. Halladay'

class NeuronGene():
    def __init__(self, id, activation_function='sigmoid', bias=0, nodeType='hidden'):
        self.id = id
        self.bias = bias
        self.activation_function = activation_function
        self.enabled = True
        self.FFWto = []
        self.FFWout = []
        self.RCto = []
        self.RCout = []
        self.Delayto = []
        self.Delayout = []
        self.layer = 0
        self.nodeType = nodeType

class FFWConnectionGene():
    def __init__(self):
        self.innovation_number = 0       
        self.source = 0       
        self.dest = 0       
        self.weight = 0       
        self.enabled = True
        self.to_output = False    


class DelayConnectionGene():
    def __init__(self):
        self.innovation_number = 0       
        self.source = 0       
        self.dest = 0       
        self.weight = 0       
        self.enabled = True       
        self.initial_value = 0
        self.delay = 0

class RCConnectionGene():
    def __init__(self):
        self.innovation_number = 0       
        self.source = 0       
        self.dest = 0       
        self.weight = 0       
        self.enabled = True       
        self.initial_value = 0

class Layer():
    def __init__(self, id, nodes=[]) -> None:
        self.nodes = nodes
        self.id = id

    def add_node(self, node):
        if(node not in self.nodes):       
            self.nodes.append(node)       
            node.layer = self.id
    
    def remove_node(self, node):
        if(node in self.nodes):   
            self.nodes.remove(node)
            if(node.layer == self.id):       
                node.layer = None       




class Population():
    """
    Defines a common context for the evolution of individual genomes
    Tracks the innovation numbers associated with genes for nodes and connections
    Defines an interface for genomes to create new nodes and connections while 
    ensuring that nodes and connections are given the proper innovation number
    """

    def __init__(self, input_shape, output_shape, population_size=100) -> None:
        '''
        Population must be initialized with an input/output shape and population size
        '''
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.population_size = population_size
        self.genomes = []

        self.neuronGenes: dict = {
            'input':[], # list of input node descriptions as a 2-tuple (innovation_number, input_number)
            'output':[], # list of output node descriptions as a 2-tuple (innovation_number, output_number)
            'hidden':[], # list of hidden node descriptions as a 2-tuple (innovation_number, connection_site_number)
        }
        self.FFWConnectionGenes: list = [] # list of FFW connection descriptions as a 3-tuple (innovation_number, source node, destination node)
        self.RCConnectionGenes: list = [] # list of RC connection descriptions as a 3-tuple (innovation_number, source node, destination node)
        self.DelayConnectionGenes: list = [] # list of delay connection descriptions as a 3-tuple (innovation_number, source node, destination node)
        self.current_node_innovation_number = 0
        self.current_FFW_innovation_number = 0
        self.current_RC_innovation_number = 0
        self.current_Delay_innovation_number = 0

    def createNeuron(self, nodeType: str, nodeSite: FFWConnectionGene = None, input_number: int = None, output_number: int = None) -> NeuronGene:
        '''
        Creates new Neuron gene with given type at nodeSite
        If a neuron has already been created at that nodeSite
        the new neuron will be given the same innovation number as the existing one
        else it will be given a new innovation number
        returns the new Neuron gene                
        '''
        node = None
        if(nodeSite is None and nodeType is 'input' and input_number is not None):
            for n in self.neuronGenes['input']:
                if(n[1] == input_number):
                    node = NeuronGene(n[0], nodeType=nodeType)
                    break
            if(node is None):
                self.current_node_innovation_number += 1
                node = NeuronGene(self.current_node_innovation_number, nodeType=nodeType)
                self.neuronGenes['input'].append((self.current_node_innovation_number, input_number))
        elif(nodeSite is None and nodeType is 'output' and output_number is not None):
            for n in self.neuronGenes['output']:
                if(n[1] == output_number):
                    node = NeuronGene(n[0], nodeType=nodeType)
                    break
            if(node is None):
                self.current_node_innovation_number += 1
                node = NeuronGene(self.current_node_innovation_number, nodeType=nodeType)
                self.neuronGenes['output'].append((self.current_node_innovation_number, output_number))
        elif(nodeSite is not None and nodeType is 'hidden'):
            # check to see if nodeSite is already a node in the population
            # if it is, then use the existing node instead of creating a new one
            for n in self.neuronGenes['hidden']:
                if(n[1] == nodeSite):
                    node = NeuronGene(n[0], nodeType=nodeType)
                    break
            if(node is None):
                self.current_node_innovation_number += 1
                node = NeuronGene(self.current_node_innovation_number, nodeType=nodeType)
                self.neuronGenes['hidden'].append((self.current_node_innovation_number, nodeSite))
        else:
            if(nodeSite is not None and nodeType is not 'hidden'):
                raise ValueError('NodeSite must be None if nodeType is input or output')
            elif(nodeSite is None and nodeType is 'hidden'):
                raise ValueError('NodeSite must be specified if nodeType is hidden')
            elif(nodeType is 'input' and input_number is None):
                raise ValueError('input_number must be specified if nodeType is input')
            elif(nodeType is 'output' and output_number is None):
                raise ValueError('output_number must be specified if nodeType is output')
            else:
                raise ValueError(f'Error in population.createNeuron. Values are nodeType: {nodeType}, nodeSite:{nodeSite}, input_number: {input_number}, and output_number: {output_number}')
        return node

    def createFFWConnection(self, source: int, destination: int) -> FFWConnectionGene:
        '''
        Creates a new connection gene from source node to destination node
        if a connection between the two nodes has already been created,
        we use the existing innovation number, otherwise we create a new one
        returns the new connection gene                             
        '''
        connection = None
        if(source is not None and destination is not None):
            for g in self.FFWConnectionGenes:                   
                if(g[1] == source and g[2] == destination):
                    connection = FFWConnectionGene(g[0], source, destination)   
                    break
            if(connection is None):                   
                connection = FFWConnectionGene(self.current_FFW_innovation_number, source, destination)                   
                self.current_FFW_innovation_number += 1
                self.FFWConnectionGenes.append((self.current_FFW_innovation_number, source, destination))
        else:
            raise ValueError('Source and destination must be specified to create a FFWconnection')
        return connection


    def createRCConnection(self, source: int, destination: int) -> RCConnectionGene:       
        '''
        Creates a new connection gene from source node to destination node
        if a connection between the two nodes has already been created,
        we use the existing innovation number, otherwise we create a new one
        returns the new connection gene
        '''
        connection = None
        if(source is not None and destination is not None):       
            for g in self.RCConnectionGenes:                   
                if(g[1] == source and g[2] == destination):       
                    connection = RCConnectionGene(g[0], source, destination)                   
                    break       
            if(connection is None):                   
                connection = RCConnectionGene(self.current_RC_innovation_number, source, destination)                   
                self.current_RC_innovation_number += 1
                self.RCConnectionGenes.append((self.current_RC_innovation_number, source, destination))         
        else:       
            raise ValueError('Source and destination must be specified to create a RCconnection')       
        return connection
        

    def createDelayConnection(self, source: int, destination: int) -> DelayConnectionGene:
        '''
        Creates a new connection gene from source node to destination node       
        if a connection between the two nodes has already been created,       
        we use the existing innovation number, otherwise we create a new one       
        returns the new connection gene
        '''       
        connection = None       
        if(source is not None and destination is not None):       
            for g in self.DelayConnectionGenes:       
                if(g[1] == source and g[2] == destination):       
                    connection = DelayConnectionGene(g[0], source, destination)       
                    break       
            if(connection is None):       
                connection = DelayConnectionGene(self.current_Delay_innovation_number, source, destination)       
                self.current_Delay_innovation_number += 1
                self.DelayConnectionGenes.append((self.current_Delay_innovation_number, source, destination))  
        else:       
            raise ValueError('Source and destination must be specified to create a delay connection')       
        return connection




class Genome():
    '''
    Directly Encodes a Nueral Network
    '''

    def __init__(self, 
        population: Population, input_nodes = None, output_nodes = None, 
        nodes = [], FFWConnections = [], DelayConnections = [], RCConnections = [], 
        layers = {}
    ):
        '''
        Constructor for the Genome class. Sets the input and output shapes. Shapes must be in 1-D format.
        Genome will be associated with a population object that determines the shape of the inputs and outputs
        and tracks the innovation numbers of its nodes and connections.
        Lists of nodes and connections can be passed in to determine the structure of the genome       
        '''

        self.input_shape = population.input_shape
        self.output_shape = population.output_shape


        
        self.layers = layers
        self.unlayered = False

        self.nodes = nodes

        if(input_nodes is None):
            self.input_nodes = [NeuronGene(i, nodeType='input') for i in range(self.input_shape[0])]
            self.unlayered = True
        else:
            self.input_nodes = input_nodes

        if(output_nodes is None):
            self.output_nodes = [NeuronGene(i, nodeType='output') for i in range(self.output_shape[0])]
            self.unlayered = True
        else:
            self.output_nodes = output_nodes


        self.node_count = len(nodes) + len(self.input_shape[0]) + len(self.output_shape[0])
        
        self.FFWConnections = FFWConnections
        self.DelayConnections = DelayConnections
        self.RCConnections = RCConnections

        if(self.unlayered):
            self.resolve_layers()

    def resolve_layers(self):
        '''
        Function will set the layer ids of all the nodes in the network by 
        conducting a breadth-first search of the nodes starting from the input
        places each node in a layer based on the distance from the input node
        '''

        # Create the input layer
        self.layers[0] = Layer(0)
        for i in range(self.input_shape[0]):
            self.layers[0].add_node(self.input_nodes[i])

        # Create the output layer
        self.layers[1] = Layer(1)
        last = 1
        for i in range(self.output_shape[0]):
            self.layers[1].add_node(self.output_nodes[i])

        # Create the hidden layers
        i = 0
        while(i < last):
            for n in self.layers[i].nodes:
                for c in n.FFWout:       
                    if(c.enabled and c.dest):
                        pass
                    pass
                pass




    def add_node(self, node):
        self.nodes.append(node)
        self.node_count += 1
    

    def add_connection(self, connection):
        self.FFWconnections.append(connection)
    

    def mutate(self):
        if(np.random.random() < 0.1):
            self.mutate_node()
        else:
            self.mutate_connection()


        def mutate_node(self):
            if(np.random.random() < 0.5):
                self.mutate_node_add()
            else:
                self.mutate_node_remove()
            

        def mutate_node_add(self):
            if(np.random.random() < 0.5):
                pass


        def mutate_node_remove(self):       
            if(np.random.random() < 0.5):
                pass


        def mutate_connection(self):
            if(np.random.random() < 0.5):
                self.mutate_connection_add()
            else:
                self.mutate_connection_remove()
        

        def mutate_connection_add(self):
            if(np.random.random() < 0.5):
                self.mutate_connection_add_ffw()
            elif(np.random.random() < 0.5):
                self.mutate_connection_add_delay()
            elif(np.random.random() < 0.5):
                self.mutate_connection_add_rc()


        def mutate_connection_add_ffw(self):
            pass
        

        def mutate_connection_add_delay(self):
            pass


        def mutate_connection_add_rc(self):
            pass


        def mutate_connection_remove(self):
            if(np.random.random() < 0.5):
                self.mutate_remove_ffw()
            elif(np.random.random() < 0.5):
                self.mutate_remove_delay()
            elif(np.random.random() < 0.5):
                self.mutate_remove_rc()


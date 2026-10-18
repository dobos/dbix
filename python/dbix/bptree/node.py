class Node:
    """Base class for B+ tree nodes"""
    
    def __init__(self, max_keys):
        """
        Initialize a node with maximum number of keys it can hold
        """
        self.max_keys = max_keys
        self.keys = []
        
    def needs_split(self):
        """Check if node is full"""
        return len(self.keys) > self.max_keys
        
    def is_empty(self):
        """Check if node is empty"""
        return len(self.keys) == 0
        
    def split(self):
        """
        Split the node into two nodes
        This method should be overridden by subclasses
        """
        raise NotImplementedError("Split method must be implemented by subclasses")
        
    def __str__(self):
        """String representation of the node"""
        return f"Node(keys={self.keys})"

    def get_formatted_keys(self):
        """Get the keys formatted as a string with exactly max_keys slots"""
        return ", ".join([str(key) for key in self.keys] + [""] * (self.max_keys - len(self.keys)))
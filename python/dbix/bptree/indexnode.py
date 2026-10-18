from .node import Node

class IndexNode(Node):
    """Index node for B+ tree that stores key intervals"""
    
    def __init__(self, max_keys):
        """
        Initialize an index node with maximum number of keys it can hold
        """
        super().__init__(max_keys)
        self.children = []  # Pointers to child nodes
        
    def split(self, split_direction='left'):
        """
        Split an index node into two index nodes
        Distribute keys and children according to split direction
        """
        # Calculate split point based on split direction
        if split_direction == 'left':
            # Left node gets one more item when even
            if self.max_keys % 2 == 0:
                split_point = self.max_keys // 2
            else:
                split_point = (self.max_keys + 1) // 2
        else:  # right
            # Right node gets one more item when even
            if self.max_keys % 2 == 0:
                split_point = self.max_keys // 2 + 1
            else:
                split_point = self.max_keys // 2
        
        # Create new index node
        new_index = IndexNode(self.max_keys)
        
        # For index nodes with max_keys=2, we have 3 children when split
        # The split should be such that we get the expected result
        if len(self.keys) > 0:
            # The promoted key is the middle key that gets moved up to parent
            promoted_key = self.keys[split_point]
            
            # Move second half of keys and children to new index node
            new_index.keys = self.keys[split_point + 1:]
            new_index.children = self.children[split_point + 1:]
            
            # Keep first half in current node
            self.keys = self.keys[:split_point]
            self.children = self.children[:split_point + 1]  # Keep the pointer to the split key
        else:
            # This shouldn't happen in normal operation, but just in case
            promoted_key = None
            new_index.keys = []
            new_index.children = []
            
        # Return the new index node and the promoted key (middle key)
        return new_index, promoted_key
        
    def insert_child(self, child_node):
        """
        Insert a child node into the index node
        """
        self.children.append(child_node)
        
    def __str__(self):
        """String representation of the index node"""
        return f"IndexNode(keys={self.keys}, children={len(self.children)})"
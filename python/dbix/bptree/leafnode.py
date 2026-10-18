from .node import Node

class LeafNode(Node):
    """Leaf node for B+ tree that stores actual data keys"""
    
    def __init__(self, max_keys):
        """
        Initialize a leaf node with maximum number of keys it can hold
        """
        super().__init__(max_keys)
        self.next_leaf = None  # Pointer to next leaf node for sequential access
        
    def split(self, split_direction='left'):
        """
        Split a leaf node into two leaf nodes
        Distribute keys according to split direction
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
            
        # Create new leaf node
        new_leaf = LeafNode(self.max_keys)
        
        # Move second half of keys to new leaf
        new_leaf.keys = self.keys[split_point:]
        self.keys = self.keys[:split_point]
        
        # Set up next pointer
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf
        
        # Return the new leaf and the key to promote
        return new_leaf, new_leaf.keys[0] if new_leaf.keys else None
        
    def insert(self, key):
        """
        Insert a key into the leaf node
        """
        # Insert in sorted order
        self.keys.append(key)
        self.keys.sort()
        
    def __str__(self):
        """String representation of the leaf node"""
        return f"LeafNode(keys={self.keys})"
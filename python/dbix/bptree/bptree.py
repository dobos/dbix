from .leafnode import LeafNode
from .indexnode import IndexNode


class BPlusTree:
    """B+ tree implementation"""
    
    def __init__(self, index_slots, leaf_slots, split_direction='left'):
        """
        Initialize B+ tree with specified slot counts for index and leaf nodes
        
        Args:
            index_slots: Number of slots in index nodes
            leaf_slots: Number of slots in leaf nodes
            split_direction: Direction for splitting nodes ('left' or 'right')
        """
        self.index_slots = index_slots
        self.leaf_slots = leaf_slots
        self.split_direction = split_direction
        self.root = LeafNode(leaf_slots)  # Start with a single leaf node
        self.height = 1
        
    def will_cause_split(self, key):
        """
        Check if inserting a key would cause a node to split
        """
        # Find the leaf node where the key would be inserted
        leaf_node = self._find_leaf(key)
        
        # Check if adding this key would make the node full
        # We need to check if the node would be full after insertion
        return len(leaf_node.keys) + 1 > leaf_node.max_keys
        
    def insert(self, key):
        """
        Insert a key into the B+ tree
        """
        # Insert into leaf node
        leaf_node = self._find_leaf(key)
        leaf_node.insert(key)
        
        # Check if leaf node needs to be split
        if leaf_node.needs_split():
            self._split_leaf(leaf_node)
            
    def _find_leaf(self, key):
        """
        Find the leaf node where the key should be inserted
        """
        current = self.root
        
        # Navigate down to the leaf level
        while isinstance(current, IndexNode):
            # Find the appropriate child
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]
            
        return current
        
    def _split_leaf(self, leaf_node):
        """
        Split a leaf node and update the tree structure
        """
        # Split the leaf node
        new_leaf, promoted_key = leaf_node.split(self.split_direction)
        
        # If we're splitting the root, we need to create a new root
        if leaf_node == self.root:
            # Create new root
            new_root = IndexNode(self.index_slots)
            new_root.keys.append(promoted_key)
            new_root.children.append(leaf_node)
            new_root.children.append(new_leaf)
            self.root = new_root
            self.height += 1
        else:
            # Find the parent node and insert the new key
            parent = self._find_parent(leaf_node)
            if parent is not None:
                # Insert the promoted key into parent
                parent.keys.append(promoted_key)
                parent.keys.sort()
                
                # Find the position of the promoted key
                pos = parent.keys.index(promoted_key)
                parent.children.insert(pos + 1, new_leaf)
                
                # Check if parent needs to be split
                if parent.needs_split():
                    self._split_index(parent)
                    
    def _find_parent(self, node):
        """
        Find the parent of a given node
        """
        if node == self.root:
            return None
            
        current = self.root
        
        # Navigate down to find the parent
        while isinstance(current, IndexNode):
            # Check if any child is the target node
            if node in current.children:
                return current
                
            # Find the appropriate child
            i = 0
            while i < len(current.keys) and node.keys[0] >= current.keys[i]:
                i += 1
            current = current.children[i]
            
        return None
        
    def _split_index(self, index_node):
        """
        Split an index node and update the tree structure
        """
        # Split the index node
        new_index, promoted_key = index_node.split(self.split_direction)
        
        # If we're splitting the root, we need to create a new root
        if index_node == self.root:
            # Create new root
            new_root = IndexNode(self.index_slots)
            new_root.keys.append(promoted_key)
            new_root.children.append(index_node)
            new_root.children.append(new_index)
            self.root = new_root
            self.height += 1
        else:
            # Find the parent node and insert the new key
            parent = self._find_parent(index_node)
            if parent is not None:
                # Insert the promoted key into parent
                parent.keys.append(promoted_key)
                parent.keys.sort()
                
                # Find the position of the promoted key
                pos = parent.keys.index(promoted_key)
                parent.children.insert(pos + 1, new_index)
                
                # Check if parent needs to be split
                if parent.needs_split():
                    self._split_index(parent)
                    
    def print_tree(self, mode="text"):
        """
        Print the tree in a readable format
        """
        if self.root is None:
            print("Empty tree")
            return
            
        # Level-order traversal to print tree
        queue = [(self.root, 0)]
        current_level = 0
        level_nodes = []
        
        while queue:
            node, level = queue.pop(0)
            
            if level != current_level:
                # Print the previous level
                self._print_level(level_nodes, mode)
                level_nodes = []
                current_level = level
                
            level_nodes.append(node)
            
            # Add children to queue for level-order traversal
            if isinstance(node, IndexNode):
                for child in node.children:
                    queue.append((child, level + 1))
                    
        # Print the last level
        if level_nodes:
            self._print_level(level_nodes, mode)
            
    def _print_level(self, nodes, mode="text"):
        """
        Print a level of the tree with proper formatting matching the example
        """
        if not nodes:
            return

        level_str = ""
        if mode == "text":
            for i, node in enumerate(nodes):
                if i > 0:
                    level_str += " "

                # Format node with exactly max_keys slots
                formatted_keys = node.get_formatted_keys()
                level_str += "[" + formatted_keys + "]"
        elif mode == "latex":
            level_str += "\\begin{equation*}\n"

            for i, node in enumerate(nodes):
                if i > 0:
                    level_str += " "

                # Format node with exactly max_keys slots
                formatted_keys = node.get_formatted_keys()
                level_str += "\\left[ " + formatted_keys + " \\right] \\quad"

            level_str += "\\end{equation*}\n"

        print(level_str.strip())
            
    def __str__(self):
        """String representation of the B+ tree"""
        return f"BPlusTree(height={self.height}, index_slots={self.index_slots}, leaf_slots={self.leaf_slots})"
import unittest
from dbix.bptree import BPlusTree


class TestBPlusTree(unittest.TestCase):
    
    def test_empty_tree(self):
        """Test creating an empty tree"""
        tree = BPlusTree(3, 4)
        self.assertIsNotNone(tree)
        self.assertEqual(tree.height, 1)
        
    def test_single_insert(self):
        """Test inserting a single element"""
        tree = BPlusTree(3, 4)
        tree.insert(5)
        # Tree should still be valid
        self.assertIsNotNone(tree.root)
        
    def test_multiple_inserts(self):
        """Test inserting multiple elements"""
        tree = BPlusTree(3, 4)
        elements = [1, 9, 12, 7, 8, 4, 5]
        
        for element in elements:
            tree.insert(element)
            
        # Tree should be valid
        self.assertIsNotNone(tree.root)
        
    def test_leaf_split(self):
        """Test that leaf nodes split correctly"""
        # Create a tree with small leaf slots to force splits
        tree = BPlusTree(3, 2)  # 2 slots in leaf nodes
        elements = [1, 2, 3, 4, 5]
        
        for element in elements:
            tree.insert(element)
            
        # Tree should be valid and have proper structure
        self.assertIsNotNone(tree.root)
        
    def test_index_split(self):
        """Test that index nodes split correctly"""
        # Create a tree with small slots to force index splits
        tree = BPlusTree(2, 4)  # 2 slots in index nodes
        elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for element in elements:
            tree.insert(element)
            
        # Tree should be valid and have proper structure
        self.assertIsNotNone(tree.root)
        
    def test_print_tree(self):
        """Test printing the tree structure"""
        tree = BPlusTree(3, 4)
        elements = [1, 9, 12, 7, 8, 4, 5]
        
        for element in elements:
            tree.insert(element)
            
        # This should not raise an exception
        try:
            tree.print_tree()
            success = True
        except Exception as e:
            success = False
            
        self.assertTrue(success)

    def test_leaf_split_well_known1(self):
        """Test printing the tree structure"""
        tree = BPlusTree(3, 2)
        elements = [1, 2]
        
        for element in elements:
            tree.insert(element)

        self.assertEqual(str(tree.root), "LeafNode(keys=[1, 2])")

    def test_leaf_split_well_known2(self):
        """Test printing the tree structure"""
        tree = BPlusTree(3, 2)
        elements = [10, 9, 6, 5, 7, 8, 3, 4]
        
        for element in elements:
            tree.will_cause_split(element)
            tree.insert(element)

        # self.assertEqual(str(tree.root), "LeafNode(keys=[1, 2])")
                

if __name__ == '__main__':
    unittest.main()
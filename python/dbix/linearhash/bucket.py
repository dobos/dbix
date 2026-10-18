class Bucket:
    """Represents a bucket in a linear hash table"""
    
    def __init__(self, max_keys):
        """
        Initialize a bucket with maximum number of keys it can hold
        
        Args:
            max_keys: Number of keys the bucket can hold
        """
        self.max_keys = max_keys
        self.keys = []
        self.overflow_buckets = []  # List of overflow buckets
        
    def insert(self, key):
        """
        Insert a key into the bucket
        
        Args:
            key: Key to insert
            
        Returns:
            True if insertion was successful, False if bucket is full
        """
        if len(self.keys) < self.max_keys:
            self.keys.append(key)
            self.keys.sort()  # Keep keys sorted
            return True
        return False
        
    def is_full(self):
        """Check if bucket is full"""
        return len(self.keys) >= self.max_keys
        
    def add_overflow_bucket(self, overflow_bucket):
        """Add an overflow bucket to this bucket"""
        self.overflow_buckets.append(overflow_bucket)

    def recycle_overflow_buckets(self):
        """Remove all overflow buckets from this bucket"""
        for i in range(len(self.overflow_buckets), 0, -1):
            if len(self.overflow_buckets[i - 1].keys) == 0:
                self.overflow_buckets.pop(i - 1)

    def print_bucket(self, mode="text", binary=False, min_key_digits=0):
        """Print the bucket contents in the required format"""
        if mode == "text":
            # Format keys with placeholders for empty slots
            formatted_keys = []
            for j in range(self.max_keys):
                if j < len(self.keys):
                    if binary:
                        if min_key_digits > 0:
                            formatted_keys.append(f"{self.keys[j]:0{min_key_digits}b}")  # Binary format with padding
                        else:
                            formatted_keys.append(f"{self.keys[j]:b}")  # Binary format
                    else:
                        formatted_keys.append(str(self.keys[j]))
                else:
                    formatted_keys.append("")
            print(f"[{', '.join(formatted_keys)}]", end="")
        elif mode == "latex":
            # Format keys with placeholders for empty slots in LaTeX
            formatted_keys = []
            for j in range(self.max_keys):
                if j < len(self.keys):
                    if binary:
                        if min_key_digits > 0:
                            formatted_keys.append(f"{self.keys[j]:0{min_key_digits}b}")  # Binary format with padding
                        else:
                            formatted_keys.append(f"{self.keys[j]:b}")  # Binary format
                    else:
                        formatted_keys.append(str(self.keys[j]))
                else:
                    formatted_keys.append("")
            print("\\begin{equation*}")
            print(f"    \\left[ {', '.join(formatted_keys)} \\right]")
            print("\\end{equation*}")
            print()
            
    def __str__(self):
        """String representation of the bucket"""
        return f"Bucket(keys={self.keys}, overflow_buckets={len(self.overflow_buckets)})"
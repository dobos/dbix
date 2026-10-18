import math
from .bucket import Bucket

class LinearHashTable:
    """Linear hash table implementation"""
    
    def __init__(self, slots_per_bucket, fill_factor):
        """
        Initialize linear hash table
        
        Args:
            slots_per_bucket: Number of slots in each bucket
            fill_factor: Maximum fill factor (total keys / all slots)
        """
        self.slots_per_bucket = slots_per_bucket
        self.fill_factor = fill_factor
        self.buckets = [Bucket(slots_per_bucket)]  # Start with single bucket
        self.number_of_buckets = 1
        self.total_keys = 0
        
    def _get_i(self):
        """Calculate i = ceil(log_2(number of buckets))"""
        return math.ceil(math.log2(self.number_of_buckets))

    def _get_r(self, total_keys = None):
        """Calculate the fill-factor r = total keys / (number of buckets * slots per bucket)"""
        total_keys = self.total_keys if total_keys is None else total_keys
        return total_keys / (self.number_of_buckets * self.slots_per_bucket)
        
    def _get_target_bucket(self, hash_value):
        """Get target bucket using i least significant bits"""
        i = self._get_i()
        # Extract i least significant bits
        target_bucket = hash_value & ((1 << i) - 1)
        
        # If target bucket doesn't exist, flip the i'th bit
        if target_bucket >= self.number_of_buckets:
            target_bucket = target_bucket ^ (1 << (i - 1))
            
        return target_bucket
        
    def insert(self, hash_value):
        """
        Insert a hash value into the linear hash table
        
        Args:
            hash_value: 8-bit hash value to insert
            
        Returns:
            True if insertion caused a split, False otherwise
        """
        # Find target bucket
        target_bucket_index = self._get_target_bucket(hash_value)
        target_bucket = self.buckets[target_bucket_index]
        
        # Try to insert into target bucket first
        if target_bucket.insert(hash_value):
            pass
        else:
            # Bucket is full, create new overflow bucket and insert there
            new_overflow_bucket = Bucket(self.slots_per_bucket)
            target_bucket.add_overflow_bucket(new_overflow_bucket)
            new_overflow_bucket.insert(hash_value)
        
        self.total_keys += 1

        # Check fill factor after insertion
        current_fill_factor = self._get_r()
        if current_fill_factor >= self.fill_factor:
            # Need to split the bucket
            self._split_bucket()
            return True  # Split occurred
        else:
            return False  # No split needed
            
    def _split_bucket(self):
        """Split a bucket and redistribute keys according to linear hash algorithm"""
        # Create new bucket
        new_bucket = Bucket(self.slots_per_bucket)
        self.buckets.append(new_bucket)
        self.number_of_buckets += 1

        i = self._get_i()
        bucket_index = (self.number_of_buckets - 1) ^ (1 << (i - 1))
        old_bucket = self.buckets[bucket_index]
        
        # Add new bucket to the list - this becomes the new bucket at index 
        # equal to the current number of buckets
        
        # Redistribute keys from old bucket
        old_bucket_keys = []
        new_bucket_keys = []
        # Iterate over the chain of buckets starting from the old bucket
        for bucket in [old_bucket] + old_bucket.overflow_buckets:
            for key in bucket.keys:
                target_after_split = key & ((1 << i) - 1)
                if target_after_split == bucket_index:
                    # Key stays in old bucket
                    old_bucket_keys.append(key)
                else:
                    # Key goes to new bucket
                    new_bucket_keys.append(key)

            # Clear the bucket's keys after redistribution
            bucket.keys = []

        # Insert back the old keys
        for key in old_bucket_keys:
            old_bucket.insert(key)

        # Remove the unused overflow buckets from the old bucket
        old_bucket.recycle_overflow_buckets()

        for key in new_bucket_keys:
            new_bucket.insert(key)
            
    def print_table(self):
        """Print the hash table in the required format"""
        i = self._get_i()
        
        # Print each bucket and its contents
        for bucket_index in range(self.number_of_buckets):
            bucket = self.buckets[bucket_index]
            
            # Calculate the hash value for this bucket (using bucket index)
            hash_value = bucket_index & ((1 << i) - 1)
            
            # Print the hash value and bucket contents
            if bucket.keys:
                print(f"{hash_value}: [{', '.join(map(str, bucket.keys))}]")
            else:
                print(f"{hash_value}: []")
            
            # Print overflow buckets if any
            if bucket.overflow_buckets:
                overflow_contents = []
                for overflow_bucket in bucket.overflow_buckets:
                    overflow_contents.append(f"[{', '.join(map(str, overflow_bucket.keys))}]")
                print(f"  Overflow: {' '.join(overflow_contents)}")
                
    def will_cause_split(self):
        """Check if inserting a hash value will cause a split"""
        # Check if fill factor would exceed threshold after insertion
        # We don't need to examine the target bucket, just calculate the fill factor
        # with the hypothetical new insertion
        current_fill_factor = self._get_r(self.total_keys + 1)
        # If we're at or above the threshold, inserting would cause a split
        return current_fill_factor >= self.fill_factor

    def print_hashtable(self, mode="text", binary=False):
        """Print the hash table in the required format"""
        i = self._get_i()
        
        # Calculate the minimum number of digits needed for binary key representation
        min_key_digits = 0
        if binary and self.total_keys > 0:
            # Find the maximum key value to determine minimum digits needed
            max_key = 0
            for bucket in self.buckets:
                for key in bucket.keys:
                    if key > max_key:
                        max_key = key
                # Check overflow buckets too
                for overflow_bucket in bucket.overflow_buckets:
                    for key in overflow_bucket.keys:
                        if key > max_key:
                            max_key = key
            # Calculate minimum digits needed (position of least significant 1-bit in max_key + 1)
            if max_key > 0:
                # Find position of the least significant 1-bit
                min_key_digits = max_key.bit_length()
            else:
                min_key_digits = 1
        
        if mode == "text":
            # Print each bucket and its contents
            for bucket_index in range(self.number_of_buckets):
                bucket = self.buckets[bucket_index]
                
                # Calculate the hash value for this bucket (using bucket index)
                hash_value = bucket_index & ((1 << i) - 1)
                
                # Print the hash value in binary if requested, otherwise decimal
                if binary:
                    # Print only the k least significant bits needed for current state
                    # k = ceil(log2(number of buckets))
                    if self.number_of_buckets > 0:
                        # Calculate number of bits needed for bucket index
                        bits_needed = i  # This is ceil(log2(number of buckets))
                        print(f"{hash_value:0{bits_needed}b}:", end=" ")
                    else:
                        print(f"{hash_value}:", end=" ")
                else:
                    print(f"{hash_value}:", end=" ")
                
                bucket.print_bucket(mode, binary=binary, min_key_digits=min_key_digits)
                
                # Print overflow buckets if any, on the same line as the head bucket (no newline)
                if bucket.overflow_buckets:
                    for overflow_bucket in bucket.overflow_buckets:
                        print(" -> ", end="")
                        overflow_bucket.print_bucket(mode, binary=binary, min_key_digits=min_key_digits)
                print()  # Add newline after the bucket and overflow buckets
        elif mode == "latex":
            # Print each bucket and its contents in LaTeX format
            for bucket_index in range(self.number_of_buckets):
                bucket = self.buckets[bucket_index]
                
                # Calculate the hash value for this bucket (using bucket index)
                hash_value = bucket_index & ((1 << i) - 1)
                
                # Print the hash value in binary if requested, otherwise decimal
                if binary:
                    # Print only the k least significant bits needed for current state
                    # k = ceil(log2(number of buckets))
                    if self.number_of_buckets > 0:
                        # Calculate number of bits needed for bucket index
                        bits_needed = i  # This is ceil(log2(number of buckets))
                        hash_value_str = f"{hash_value:0{bits_needed}b}"
                    else:
                        hash_value_str = str(hash_value)
                else:
                    hash_value_str = str(hash_value)
                
                # Print the hash value and bucket contents in LaTeX with all buckets in same equation
                if bucket.keys:
                    # Format keys with placeholders for empty slots
                    formatted_keys = []
                    for j in range(self.slots_per_bucket):
                        if j < len(bucket.keys):
                            if binary:
                                formatted_keys.append(f"{bucket.keys[j]:0{min_key_digits}b}")  # Binary format with padding
                            else:
                                formatted_keys.append(str(bucket.keys[j]))
                        else:
                            formatted_keys.append("")
                    print("\\begin{equation*}")
                    print(f"    {hash_value_str}: \\left[ {', '.join(formatted_keys)} \\right]")
                    # Add overflow buckets in the same equation
                    if bucket.overflow_buckets:
                        for overflow_bucket in bucket.overflow_buckets:
                            # Format overflow bucket keys with placeholders for empty slots
                            formatted_overflow_keys = []
                            for k in range(self.slots_per_bucket):
                                if k < len(overflow_bucket.keys):
                                    if binary:
                                        formatted_overflow_keys.append(f"{overflow_bucket.keys[k]:0{min_key_digits}b}")  # Binary format with padding
                                    else:
                                        formatted_overflow_keys.append(str(overflow_bucket.keys[k]))
                                else:
                                    formatted_overflow_keys.append("")
                            print(f"    \\rightarrow \\left[ {', '.join(formatted_overflow_keys)} \\right]")
                    print("\\end{equation*}")
                    print()
                else:
                    # Format empty bucket with placeholders
                    formatted_keys = [" " for _ in range(self.slots_per_bucket)]
                    print("\\begin{equation*}")
                    print(f"    {hash_value_str}: \\left[ {', '.join(formatted_keys)} \\right]")
                    # Add overflow buckets in the same equation
                    if bucket.overflow_buckets:
                        for overflow_bucket in bucket.overflow_buckets:
                            # Format overflow bucket keys with placeholders for empty slots
                            formatted_overflow_keys = []
                            for k in range(self.slots_per_bucket):
                                if k < len(overflow_bucket.keys):
                                    if binary:
                                        formatted_overflow_keys.append(f"{overflow_bucket.keys[k]:0{min_key_digits}b}")  # Binary format with padding
                                    else:
                                        formatted_overflow_keys.append(str(overflow_bucket.keys[k]))
                                else:
                                    formatted_overflow_keys.append("")
                            print(f"    \\rightarrow \\left[ {', '.join(formatted_overflow_keys)} \\right]")
                    print("\\end{equation*}")
                    print()
Implementation of a cache with the LRU eviction scheme 

    1. The cache supports the following operations:
        - insert item
        - update item
        - remove items
        - remove all expired items
        - get the top N most frequently accessed keys
        
    2.  A hash map is used for the lookup of keys, and a list for storing values
    
    3. Recently accessed keys are moved to the beginning of the list and the cache has a maximum size of items it can hold. 

    4. A cache miss results in an exception - the entry is read from the datastore and written to cache 
    
    5. The least recently used cache eviction scheme is used to remove items from the cache


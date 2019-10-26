Implementation of a cache 

    1. Supports the following operations:
        - insert item
        - update item
        - remove items
        - remove all expired items
        - get the top N most frequently accessed keys
        
    2. Uses a hash map for O(1) lookup of keys, and a list for storing values
    
    3. Recently accessed keys are moved to the beginning of the list and the
    cache has a maximum size of items it can hold. 

    4. A cache miss results in an exception - the entry is read from the datastore and written to cache 
    
    5. The least recently used cache eviction scheme is used to remove items from the cache



A Python list, is actually an array:
List in Python is not implemented as the usual single-linked list. List in Python is, an array. That is, you can retrieve an element in a list using index with constant time O(1), without searching from the beginning of the list. What’s the implication of this? A Python developer should think for a moment when using insert() on a list object. For example:>>> list.insert(0, element)
That is not efficient when inserting an element at the front, because all the subsequent index in the list will have to be changed. You can, however, append an element to the end of the list efficiently using list.append(). Pick deque, however, if you want fast insertion or removal at both ends. It is fast because deque in Python is implemented as double-linked list. 
https://www.monitis.com/blog/python-performance-tips-part-1/

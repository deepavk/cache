import datetime
import logging
from collections import deque
from custom_exceptions import CacheMissException


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

data_store = {"key_1": "value_1",
              "key_2": "value_2",
              "key_3": "value_3",
              "key_4": "value_4",
              "key_5": "value_5",
              "key_6": "value_5",
              "key_7": "value_5",
              "key_8": "value_5",
              "key_9": "value_5",
              "key_10": "value_10"}

DEFAULT_EXPIRY = 30


class CacheItem(object):

    def __init__(self, key, value, expires_in=DEFAULT_EXPIRY):
        self.key = key
        self.value = value
        self.created_at = datetime.datetime.now()
        self.last_accessed = datetime.datetime.now()
        self.expires_at = self.last_accessed + \
                          datetime.timedelta(seconds=expires_in)

    def __str__(self):
        return "Cached Item: Key:{}, value:{}, last_accessed:{}".\
            format(self.key, self.value, self.last_accessed)

    def __repr__(self):
        return '{}({},{})'.\
            format(self.__class__.__name__, self.key, self.value)

    def set_last_accessed_at(self):
        self.last_accessed = datetime.datetime.now()

    def set_expires_at(self, expiry_datetime):
        self.expires_at = expiry_datetime

    def has_expired(self):
        now = datetime.datetime.now()
        return self.expires_at <= now


class LRUCache(object):
    
    def __init__(self, max_size):
        self.max_size = max_size
        self.item_count = 0
        self.items = deque()
        self.items_hash = {}

    def _insert_item(self, cache_item, expires_in):
        cache_item.set_last_accessed_at()
        self.items_hash[cache_item.key] = cache_item
        self.items.appendleft(cache_item)
        self._update_item_count(1)

    def _is_cache_at_max_size(self):
        return self.max_size == self.item_count

    def get_item(self, cache_key):
        cached_item = self.items_hash.get(cache_key, None)
        if not cached_item:
            raise CacheMissException("Cache miss for {}".format(cache_key))
        return cached_item

    def insert_item(self, cache_key, value, expiry=DEFAULT_EXPIRY):
        """
            if key is in hash_map - remove element and re-insert element
             at the beginning of the cached list
            else check length of cached list & pop if len is max_size,
            add item to beginning of the list
        """
        cached_item = self.items_hash.get(cache_key, None)
        if cached_item:
            self.remove_item(cached_item)
            self._insert_item(cached_item, expiry)
        else:
            if self._is_cache_at_max_size():
                item = self.items.pop()
                self._update_item_count(-1)
                logger.info("Removed item from cache {} at {}".
                            format(item, datetime.datetime.now()))
            cached_item = CacheItem(cache_key, value, expiry)
            self._insert_item(cached_item, expiry)
        return cached_item

    def remove_item(self, key):
        try:
            item = self.items_hash[key]
            self.items.remove(item)
            del self.items_hash[key]
            self._update_item_count(-1)
            logger.info("Removed item {}".format(item))
        except KeyError:
            logger.info("Item {} not found".format(key))
            return None

    def get_most_frequently_accessed(self, n):
        return [itm for idx, itm in enumerate(self.items) if idx < n]

    def remove_expired_items(self):
        for cached_item in [_itm for _itm in self.items if _itm.has_expired()]:
            self.remove_item(cached_item.key)

    def _update_item_count(self, count):
        self.item_count += count
        print(self.item_count)

    def display_items(self):
        logger.info("\nCurrent cache size:{} "
                    "and cache contents:\n".format(self.item_count))
        for itm in self.items:
            logger.info(itm)


def setup_cache():
    lru = LRUCache(3)

    # test: inserts 3 items out of 4 in the data store
    keys_to_insert = ["key_1", "key_2", "key_3"]
    for k in keys_to_insert:
        lru.insert_item(k, data_store[k])

    lru.display_items()

    # test: remove key_2, key_3, key_1 remain in cache
    lru.remove_item("key_2")
    lru.display_items()

    # test : cache miss
    key = "key_10"
    retrieve_item(lru, key)
    lru.display_items()

    logger.info("item count:{} items: {}".format(lru.item_count, len(lru.items)))
    return lru


def retrieve_item(lru, key):
    try:
        lru.get_item(key)
    except CacheMissException:
        # read value from database and insert item
        value = data_store[key]
        inserted_item = lru.insert_item(key, value)
        inserted_item.set_last_accessed_at()


if __name__ == "__main__":
    lru = setup_cache()
    # purge activity
    lru.remove_expired_items()


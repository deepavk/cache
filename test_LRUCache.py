import datetime
from unittest import TestCase
from lru_cache import LRUCache, CacheItem, data_store, DEFAULT_EXPIRY
from custom_exceptions import CacheMissException


class TestLRUCache(TestCase):
    def setUp(self):
        self.max_size = 3
        self.lru = LRUCache(self.max_size)
        for i in data_store.keys():
            self.lru.insert_item(i, data_store[i])

    def test_create_cache_item(self):
        cache_item = CacheItem(1, "one")
        self.assertIsInstance(cache_item, CacheItem)
        self.assertEqual(cache_item.key, 1)
        self.assertEqual(cache_item.value, "one")

    def test_create_lru_cache(self):
        self.assertIsInstance(self.lru, LRUCache)

    def test_insert_item(self):
        self.assertEqual(self.lru._is_cache_at_max_size(), True)
        self.assertIsInstance(self.lru.items[0], CacheItem)

    def test_insert_item_cache_at_max(self):
        self.assertEqual(self.lru._is_cache_at_max_size(), True)
        most_recent = self.lru.insert_item(3, "element3")
        cached_item = self.lru.get_most_frequently_accessed(1)[0]
        self.assertEqual(cached_item, most_recent)

    def test_get_item_hit(self):
        self.lru.insert_item("key_1", "value_1")
        cached_item = self.lru.get_item("key_1")
        self.assertEqual(cached_item.key, "key_1")
        self.assertEqual(cached_item.value, "value_1")

    def test_get_item_miss(self):
        with self.assertRaises(CacheMissException):
            self.lru.get_item("InvalidKey")

    def test_purge_items(self):
        for item in self.lru.items:
            item.set_expires_at(datetime.datetime.now() -
                                datetime.timedelta(seconds=30))

        self.lru.remove_expired_items()
        self.assertEqual(0, self.lru.item_count)

    def test_cache_operations(self):
        lru = LRUCache(3)
        # Insert items
        keys_to_insert = ["key_1", "key_2", "key_3"]
        for k in keys_to_insert:
            v = data_store[k]
            cache_item = lru.insert_item(k, v)
            self.assertIn(k, lru.items_hash)
            self.assertEqual(cache_item.key, k)
            self.assertEqual(cache_item.value, v)
        self.assertEqual(lru.item_count, 3)

        # Remove items
        lru.remove_item("key_1")
        self.assertEqual(lru.item_count, 2)
        self.assertNotIn("key_1", lru.items_hash)

        # test cache miss
        key = "key_10"
        try:
            lru.get_item(key)
        except CacheMissException:
            # read value from database and insert item into cache
            value = data_store[key]
            inserted_item = lru.insert_item(key, value, expiry=DEFAULT_EXPIRY)
            self.assertEqual(inserted_item.key, key)
            self.assertEqual(inserted_item.value, data_store[key])
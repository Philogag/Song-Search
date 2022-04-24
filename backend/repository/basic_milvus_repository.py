from pymilvus import (
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from pymilvus.orm import utility
from pymilvus.orm.exceptions import SchemaNotReadyException

from backend.utility.singleton_helper import singleton_class


class MilvusCollectionOrm:
    __collection_name__ = ''
    __schema_description__ = ''

    __auto_field_count__ = 0

    fields = []
    index = {}

    def __init__(self):
        self.schema = None
        self.collection = None
        try:
            self.init()
        except SchemaNotReadyException:
            self.reset_collection()
            self.init()

    def reset_collection(self):
        print("reset collection:", self.__collection_name__)
        utility.drop_collection(self.__collection_name__)
        self.init()

    def init(self):
        self.schema = CollectionSchema(self.fields, self.__schema_description__)
        self.collection = Collection(self.__collection_name__, self.schema, using='default', consistency_level="Strong")
        # for field, params in self.index.items():
        #     self.collection.create_index(field, params)
        self.__refresh_insert_cache()

    def __refresh_insert_cache(self):
        self.insert_cache = [[] for _ in range(len(self.fields) - self.__auto_field_count__)]

    def insert(self, data):
        assert len(data) == len(self.insert_cache), '数据格式不符'
        for i, d in enumerate(data):
            self.insert_cache[i].append(d)

    def commit(self):
        if len(self.insert_cache[0]) <= 0:
            return  # empty
        self.collection.insert(self.insert_cache)
        self.__refresh_insert_cache()

    def _search(self, search_params):
        self.collection.load()
        results = self.collection.search(
            **search_params
        )
        self.collection.release()
        return results

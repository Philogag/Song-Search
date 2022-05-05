from typing import List

from pymilvus import (
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from pymilvus.orm import utility
from pymilvus.orm.exceptions import SchemaNotReadyException


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
        if len(self.collection.indexes) <= 0:
            for field, params in self.index.items():
                self.collection.create_index(field, params)
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

    def _search(self, search_params, id_field: str, output_fields: List[str]):
        self.collection.load()
        try:
            hit_ids = self.collection.search(
                **search_params
            )
            results = []
            for hit in hit_ids:
                extra_list = self.collection.query(
                    expr=f"{id_field} in {hit.ids}",
                    output_fields=output_fields,
                    consistency_level="Strong"
                )
                result = []
                for extra, d in zip(extra_list, hit.distances):
                    result.append({
                        **extra,
                        "distances": d,
                    })
                results.append(result)
        finally:
            self.collection.release()
        return results

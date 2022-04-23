import logging
import os.path
from typing import Iterable
from jiayan import load_lm, CharHMMTokenizer
from gensim.models.word2vec import KeyedVectors

from numpy import dot, array
from gensim import matutils
from pymilvus import FieldSchema, DataType

from backend.algorithm.utility import get_or_create_model_meta, get_train_data_by_last_trained_at, uuid_to_double_int64
from backend.factory import message_queue
from backend.repository.basic_milvus_repository import MilvusCollectionOrm
from backend.utility.singleton_helper import singleton_class


def __get_abs_path(path_str: str):
    folder, _ = os.path.split(os.path.abspath(__file__))
    return os.path.join(folder, path_str)


with open(__get_abs_path('dots_stopwords.txt'), 'r', encoding='utf-8') as f:
    stop_words = f.read().split("\n")

# 分词引擎
lm = load_lm(__get_abs_path('jiayan.klm'))
tokenizer = CharHMMTokenizer(lm)

# 词向量空间
word_vector_space = KeyedVectors.load(__get_abs_path('w2v.mod'), mmap='r')

model_meta = get_or_create_model_meta(
    model_id=1,
    model_name="jiayan+word2vec+cos",
)


def sentences_to_words(content: str) -> Iterable[str]:
    """分词"""
    return [
        w for w in tokenizer.tokenize(content.strip()) if (
            w not in stop_words
            and word_vector_space.wv.has_index_for(w)
        )
    ]


def words_to_vector(words: Iterable[str]):
    """词向量，已归一化，可用内积dot代替余弦"""
    return matutils.unitvec(
        word_vector_space.wv[words]
        .mean(axis=0)
    )


@singleton_class
class SongsVectorCollection(MilvusCollectionOrm):
    __collection_name__ = 'songs_vector'
    __schema_description = '诗词向量数据集'
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="model_id", dtype=DataType.INT64),
        FieldSchema(name="uuid_p1", dtype=DataType.INT64),
        FieldSchema(name="uuid_p2", dtype=DataType.INT64),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=100)
    ]
    index = {
        "vector": {
            "metric_type": "IP",  # 距离计算：内积
            "index_type": "FLAT",  # 加速矢量搜索的索引类型
        }
    }
    __auto_field_count__ = 1

    def search(self, model_id, data, limit: int = 20):
        return self._search({
            "data": data,
            "anns_field": "vector",
            "expr": "model_id == %d"%model_id,
            "limit": limit,
            "output_fields": ['model_id', 'uuid_p1', 'uuid_p2'],
            "round_decimal": 3,
            "consistency_level": "Strong",
        })


@message_queue.data_unpacker()
def prepare_vector_set():
    """准备数据集"""
    global model_meta
    model_meta = get_or_create_model_meta(model_id=model_meta.model_id)
    data_rows = get_train_data_by_last_trained_at(model_meta)
    logging.info("Train data len: %d"%len(data_rows))
    for data in data_rows:
        sentences = sentences_to_words(data.content)
        vector = words_to_vector(sentences)
        SongsVectorCollection().insert([
            model_meta.model_id,
            *uuid_to_double_int64(data.id),
            vector,
        ])
        # print(data.title)
    SongsVectorCollection().commit()
    print("Done.")


@message_queue.data_unpacker()
def search_text(search_text: str):
    """搜索"""
    words = sentences_to_words(search_text)
    vector = words_to_vector(words)

    results = SongsVectorCollection().search(
        model_id=model_meta.model_id,
        data=vector,
        limit=20,
    )
    print(results)
    return


message_queue_register = [
    message_queue.register_listener(channel='jiayan+word2vec+cos', method='train', callback=prepare_vector_set),
    message_queue.register_listener(channel='jiayan+word2vec+cos', method='search', callback=search_text)
]

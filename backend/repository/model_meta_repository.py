from backend.data.transaction import Transaction
from backend.model.edit.model_meta_em import ModelMetaEm
from backend.model.entity.model_meta_entity import ModelMetaEntity
from backend.repository.basic_repository import BasicRepository


class ModelMetaRepository(BasicRepository):
    __entity_cls__ = ModelMetaEntity
    __model_cls__ = ModelMetaEm

    @classmethod
    def get_or_create_model_meta(cls, data: ModelMetaEm, transaction: Transaction) -> ModelMetaEm:
        if cls.check_entity_exist({"model_id": data.model_id}):
            return cls.get_first_entity_by_params({"model_id": data.model_id})
        else:
            data.id = cls.create_entity(data, transaction)
            return data

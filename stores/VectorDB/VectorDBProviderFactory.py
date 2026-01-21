from .providers.QdrantDBProvider import QdrantDBProvider
from .VectorDBenums import VectorDBenums
from controllers.BaseController import BaseController

class VectorDBFactory:
    def __Init__(self,config):
        self.config = config
        self.base_controller = BaseController()
    def create(self,provider:str):
        if provider == VectorDBenums.QDRANT.value:
            db_path = self.base_controller.get_database_path(database_name=self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE
            )
        return None
    
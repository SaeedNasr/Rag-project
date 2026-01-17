from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls,db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_ASSET_NAME.value
        ]

        indexes = Asset.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'],
                name=index['name'],
                unique=index['unique']
            )

    async def create_asset(self, asset:Asset):
        doc = asset.model_dump(exclude={'id'}, by_alias=True)
        result = await self.collection.insert_one(doc)
        return Asset(id=result.inserted_id, **{k: v for k, v in doc.items() if k != '_id'})

    async def get_all_assets(self, asset_project_id: str):
        cursor = self.collection.find({"asset_project_id": ObjectId(asset_project_id) if asset_project_id.isinstance(str) else asset_project_id})
        assets = [Asset(**asset) async for asset in cursor]
        return assets
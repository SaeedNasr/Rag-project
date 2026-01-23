from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId 
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value] 

    @classmethod
    async def create_instance(cls,db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    #async def init_collection(self):
        #all_collections = await self.db_client.list_collection_names()
        #if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            #self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value] 
            #indexes = DataChunk.get_indexes()
            #for index in indexes:
                #await self.collection.create_index(index['key'],name = index['name'],unique=index['unique'])
    #commented above block to always create indexes
    async def init_collection(self):
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_CHUNK_NAME.value
        ]

        indexes = DataChunk.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'],
                name=index['name'],
                unique=index['unique']
            )


    async def create_chunk(self, data_chunk:DataChunk):
        doc = data_chunk.model_dump(exclude={'id'}, by_alias=True)
        result = await self.collection.insert_one(doc)
        # Return new DataChunk instance with the inserted _id
        return DataChunk(id=result.inserted_id, **{k: v for k, v in doc.items() if k != '_id'})

    async def get_chunk(self, chunk_id:str):
        record = await self.collection.find_one({"_id":ObjectId(chunk_id)})
        if record:
            return DataChunk(**record)
        return None
    
    async def insert_many_chunks(self, chunks:list,batch_size:int =100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            docs = [InsertOne(chunk.model_dump(exclude={'id'}, by_alias=True)) for chunk in batch]
            await self.collection.bulk_write(docs)

        return len(chunks)
    
    async def delete_chunks_by_project(self, project_id:ObjectId):
        result = await self.collection.delete_many({"chunk_project_id":project_id})
        return result.deleted_count
    
    async def get_chunks_by_project_id(self,project_id:ObjectId,page_no:int=1,page_size:int=50):

        effective_page = max(1, page_no)
        skip_count = (effective_page - 1) * page_size

        records = await self.collection.find({
            "chunk_project_id" :project_id
        }).skip(
            skip_count
            ).limit(page_size).to_list(length = None)
        
        return [DataChunk(**record) for record in records]
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] 

    @classmethod
    async def create_instance(cls,db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    # async def init_collection(self):
    #     all_collections = await self.db_client.list_collection_names()
    #     if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
    #         self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] 
    #         indexes = Project.get_indexes()
    #         for index in indexes:
                #await self.collection.create_index(index['key'],name = index['name'],unique=index['unique'])
    # commented above block to always create indexes
    async def init_collection(self):
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_PROJECT_NAME.value
        ]

        indexes = Project.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'],
                name=index['name'],
                unique=index['unique']
            )

    

    async def create_project(self, project:Project):
        doc = project.model_dump(exclude={'id'}, by_alias=True)
        result = await self.collection.insert_one(doc)
        # Return new Project instance with the inserted _id
        return Project(id=result.inserted_id, **{k: v for k, v in doc.items() if k != '_id'})
    
    async def get_or_create_project(self, project_id:str):
        record = await self.collection.find_one({"project_id":project_id})
        if record is None:
            new_project = Project(project_id=project_id)
            return await self.create_project(new_project)
        return Project(**record)

    async def get_all_projects(self, page:int =1,page_size:int = 10):
        total_documents = await self.collection.count_documents({})
        total_pages = total_documents//page_size + (1 if total_documents % page_size > 0 else 0)
        curser = self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects = [Project(**project)async for project in curser]
        
        return projects , total_pages
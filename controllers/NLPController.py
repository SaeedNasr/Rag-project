from .BaseController import BaseController
from models.db_schemes import Project ,DataChunk
from typing import List
from stores.llm.LLMenums import DocumentTypeEnum
import json

class NLPController(BaseController):
    def __init__(self,vectordb_client,embedding_client,generation_client):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.embedding_client=embedding_client
        self.generation_client = generation_client

    #to unify the names of the collections or how it's being created !
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    

    def reset_vector_db_collection(self,project : Project):
        collection_name  = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name = collection_name)

    def get_vector_db_collection_info(self,project:Project):
        collection_name  = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        return json.loads(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )
    
    def index_into_vector_db(self,project:Project,chunks:List[DataChunk],chunks_ids :List[int],do_reset:bool =False):
        #1: get collection name
        collection_name  = self.create_collection_name(project_id=project.project_id)
        #2:manage chunks
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]

        vectors = [
            self.embedding_client.embed_text(texts=text,document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        #3:create collection if not exists 
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size = self.embedding_client.embeddings_size,
            do_reset=do_reset 
        )
        #4:insert into vector database
        _ = self.vectordb_client.insert_many(collection_name=collection_name,
                                         record_ids=chunks_ids,
                                         texts=texts,
                                         vectors=vectors,
                                         metadata=metadata)

        return True
    
    def search_vector_db_collection(self,project:Project,texts:str,limit:int =10):
        #1:get collection name 
        collection_name  = self.create_collection_name(project_id=project.project_id)
        #2:embd the text
        vector = self.embedding_client.embed_text(texts=texts,document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False
        #3:search in the vector db
        results = self.vectordb_client.search_by_vector(collection_name = collection_name,vector=vector,limit=limit)

        if not results:
            return False

        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )

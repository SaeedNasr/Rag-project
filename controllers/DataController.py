from fastapi import UploadFile
from models import ResponseSignal
from .BaseController import BaseController
from .ProjectController import ProjectController
import re
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED
        
        if file.size > self.app_settings.MAX_FILE_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED
        return True, ResponseSignal.FILE_VALID.value
    def generate_unique_file_name(self,original_filename:str,project_id:str):
        random_key = super().generate_file_name()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(original_filename)
        new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)
        while os.path.exists(new_file_path):
            random_key = super().generate_file_name()
            new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)

        return new_file_path

    def get_clean_file_name(self,original_filename:str):
        cleaned_name = re.sub(r'[^\w.]', ' ', original_filename.strip())
        cleaned_name = cleaned_name.replace(' ', '_')

        return cleaned_name
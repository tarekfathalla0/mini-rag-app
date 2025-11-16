from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # 1 MB in bytes

    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_Types:
            return False, ResponseSignal.FILE_TYPE_INVALID.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self, original_filename: str, project_id: str) -> str:
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleanded_filename = self.get_clean_filename(
            original_filename=original_filename,
        )

        new_filepath = os.path.join(
            project_path,
            random_key + "_" + cleanded_filename
        )

        while os.path.exists(new_filepath):
            random_key = self.generate_random_string()
            new_filepath = os.path.join(
                project_path,
                random_key + "_" + cleanded_filename
            )
        
        return new_filepath, random_key + "_" + cleanded_filename
    
    def get_clean_filename(self, original_filename: str) -> str:
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', original_filename.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
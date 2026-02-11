from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully."
    FILE_TYPE_INVALID = "Invalid file type."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_UPLOAD_SUCCESS = "file upload succeeded."
    FILE_UPLOAD_FAILED = "File upload failed."
    FILE_PROCESSING_SUCCESS = "File processing successful."
    FILE_PROCESSING_FAILED = "File processing failed."
    NO_FILES_TO_PROCESS = "No files to process."
    FILE_ID_ERROR = "no file found for the provided file ID."
    PROJECT_NOT_FOUND_ERROR = "Project with id {project_id} not found."
    INSERT_INTO_VECTOR_DB_FAILED = "Failed to insert data into vector database."
    INSERT_INTO_VECTOR_DB_SUCCESS = "Data inserted into vector database successfully."
    VECTORDB_COLLECTION_RETRIEVED = "vectordb collection retrieved"
    VECTORDB_SEARCH_ERROR = "vector db search error"
    VECTORDB_SEARCH_SUCCESS = "vector db search success"
from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully."
    FILE_TYPE_INVALID = "Invalid file type."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_UPLOAD_SUCCESS = "file upload succeeded."
    FILE_UPLOAD_FAILED = "File upload failed."
    FILE_PROCESSING_SUCCESS = "File processing successful."
    FILE_PROCESSING_FAILED = "File processing failed."
from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validation successful."
    FILE_TYPE_INVALID = "Invalid file type."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_UPLOAD_SUCCESS = "Success."
    FILE_UPLOAD_FAILED = "File upload failed."

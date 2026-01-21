from enum import Enum

class VectorDBenums(Enum):
    QDRANT = "QDRANT"
    
class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"
import uuid

def generate_unique_id() -> str:
    """
    Generate a unique identifier.
    
    :return: Unique UUID as a string
    """
    return str(uuid.uuid4())
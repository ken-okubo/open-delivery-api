import uuid


"""To make items creation easier to test"""


def generate_uuid():
    return {"id": str(uuid.uuid4())}

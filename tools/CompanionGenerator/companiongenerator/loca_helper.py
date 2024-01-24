from uuid import uuid4


def generate_handle():
    reg_uuid = "h" + str(uuid4())
    return reg_uuid.replace("-", "g")

VALID_PAYLOAD = {
    "type_": "email",
    "template": "test_template",
    "is_regular": True,
    "subject": "string",
    "to_role": ["string"],
    "to_id": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    "params": {"name": "Arthas"},
}

MISSING_TEMPLATE_PAYLOAD = {
    "type_": "email",
    "template": "some_wrong_template_name",
    "is_regular": True,
    "subject": "string",
    "to_role": ["string"],
    "to_id": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    "params": {"name": "Arthas"},
}

WRONG_PARAMS_PAYLOAD = {
    "type_": "email",
    "template": "test_template",
    "is_regular": True,
    "subject": "string",
    "to_role": ["string"],
    "to_id": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    "params": {"surname": "Arthas"},
}

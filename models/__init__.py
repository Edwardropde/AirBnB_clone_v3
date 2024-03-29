#!/usr/bin/python3
"""
Instantiates storage object

instantiates a database storage engine (DBStorage) if environmental
variable HBNB_TYPE_STORAGE is set to db
else instantiates file storage engine FileStorage
"""
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()

#!/usr/bin/python3
"""Defines filestorage class"""
import json


class FileStorage:
    """
    Represents abtracted storage engine

    Attributes:
        __objects (dict): dictionary of instantiated obj
        __file_path (str): name of file to save objects to
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns list: list of __object"""
        my_dict = {}
        if cls:
            for key, value in self.__objects.items():
                if key.startswith(str(cls.__name__)):
                    my_dict[key] = value
        else:
            my_dict = self.__objects
        return my_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object from __objects if found"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del(self.__objects[key])
                self.save()

    def close(self):
        """Call reload() to deserialize the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Return object based on class and ID

        Args:
            cls: specified class of object
            id: String representing object ID

        Returns:
            Object based on class and specified ID. None if not found
        """
        key = cls.__name__ + '.' + id
        return self.__objects.get(key)

    def count(self, cls=None):
        """
        Count number of objects in storage matching specific class

        Args:
            cls: Class

        Returns:
            Number of objects in storage.
            Suppose class is not passed, returns count of objects in storage
        """
        if cls is not None:
            return sum(1 for key in self.__objects if cls == self.__objects[key].__class__)
        return len(self.__objects)

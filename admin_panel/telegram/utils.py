import uuid
import os


def get_unique_file_path(instance, filename):
    """Создание уникального имени для файла"""
    extension = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join(instance._meta.model_name, unique_filename)

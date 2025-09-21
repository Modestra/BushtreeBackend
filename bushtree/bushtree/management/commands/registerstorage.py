from typing import Any
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bushtree.models import MediaRegistration
from bushtree.serializers import MediaImagesSerializer

class Command(BaseCommand):

    help = "Регистрация загруженных вручную изображений из media"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        print(f"Загрузка данных из {settings.MEDIA_ROOT}")
        for dirpath, dirnames, filenames in os.walk(settings.MEDIA_ROOT):
            parent_dir = os.path.split(dirpath)[-1]
            print(f"Текущая папка: {dirpath}")
            print(f"Родительская папка: {parent_dir}")
            print(f"Дочерние папки: {dirnames}")
            print(f"Файлы: {filenames[:10]}")
            print("-" * 30)
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                relative_path = os.path.relpath(full_path, start=settings.MEDIA_ROOT)
                MediaRegistration.objects.get_or_create(basedir=parent_dir, filename=relative_path)


                
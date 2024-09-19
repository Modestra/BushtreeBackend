from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings
from bushtree.storages import (MediaStorage, StaticStorage)
from bushtree.storages import Storage

class Command(BaseCommand):

    help = "Комманды для взаимодействия S3 хранилищем"

    def handle(self, *args: Any, **options: Any) -> str | None:
        
        if settings.USE_S3:
            print("Загрузка файлов с S3 в медиа...")
            Storage.download_file()

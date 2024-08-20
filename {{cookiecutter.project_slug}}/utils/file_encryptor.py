from abc import ABC, abstractmethod
import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
import os
import re

import logging
logger = logging.getLogger(__name__)

class AccessClassification(models.IntegerChoices):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED  = 4

    @classmethod
    def get_choices(cls):
        return [
            cls.PUBLIC,
            cls.INTERNAL,
            cls.CONFIDENTIAL,
            cls.RESTRICTED,
        ]

class FileType:
    CATCH = 0 #catch all
    UPLOAD = 1
    BENEFIT_TRANSACTION_SET = 2
    PORTFOLIO_INDEX = 3

    @classmethod
    def requires_uid(cls, file_type):
        # returns list of upload
        return file_type in [cls.CATCH, cls.UPLOAD]

class FileEncryptor(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.prefix, self.token, *_ = filename.split("_")
        decrypted_prefix = FileEncryptor.decrypt_prefix(self.prefix)
        self.file_type = decrypted_prefix.get("f", FileType.CATCH) 
        self.access_classification = decrypted_prefix.get("a", AccessClassification.RESTRICTED) 
        self.owner_pk = decrypted_prefix.get("u", 0) 

    @staticmethod
    def decrypt_prefix(filename):
        prefix = filename.split("_")[0]
        pattern = r'([a-z]+)(\d+)'
        matches = re.findall(pattern, prefix)
        result = {}
        for match in matches:
            char, integer = match
            result[char] = int(integer)
        return result

    @staticmethod
    def encrypt_prefix(
        filetype_prefix=FileType.CATCH, 
        owner_pk=0, 
        access_classification=AccessClassification.RESTRICTED
        ):
        owner_pk=owner_pk or 0
        return f"f{filetype_prefix}u{owner_pk}a{access_classification}"

    @property
    def owner(self):
        owner_pk = self.owner_pk if self.owner_pk>0 else 1 #anonymoususer
        return get_user_model().objects.get(pk=owner_pk)

    def get_filename(self):
        return self._filename

    @classmethod
    def create_filename(cls, 
            original_filename, 
            token=0,
            owner_pk=0, 
            file_type=FileType.CATCH, 
            access_classification=AccessClassification.INTERNAL, 
            **extra_data
            ) -> str:
        """
        Need to pass:
            owner_id
        """
        filename, extension = os.path.splitext(original_filename)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        encrypted_prefix = FileEncryptor.encrypt_prefix(file_type, owner_pk, access_classification)

        trailing_data = []
        if extra_data:
            trailing_data += list(extra_data.values())
        trailing_data.append(timestamp)
        trailing_data = "_".join(trailing_data)

        filename = f"{encrypted_prefix}_{token}_{trailing_data}{extension}"
        logger.info(filename)
        return filename
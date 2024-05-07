from typing import Any
from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254, null=False, blank=False)


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
from django.db import models

class BV_Register(models.Model):

    username    = ""
    password    = ""
    firstname   = ""
    lastname    = ""
    description = ""
    profile_image = ""

    class Meta:
        managed = False

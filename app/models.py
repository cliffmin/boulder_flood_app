import datetime
from flask import url_for
from app import db
from slugify import slugify
import random

class Helper(db.Document):

    name = db.StringField(max_length=255, required=True, unique=True)
    skill = db.StringField(max_length=255, required=True)
    availability = db.DateTimeField(required=False)
    location = db.StringField(required=True)
    slug = db.StringField(required=False)

    def __unicode__(self):
        return self.name

    def clean(self):
        self.slug = slugify(self.name)


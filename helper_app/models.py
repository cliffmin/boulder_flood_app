import datetime
from flask import url_for
from app import db
from slugify import slugify
import random

class Dinosaurs(db.Document):

    name = db.StringField(max_length=255, required=True, unique=True)
    dinosaur_type = db.StringField(max_length=255, required=False)
    height = db.StringField(max_length=255, required=False)
    imageURL = db.StringField(required=False)
    slug = db.StringField(required=False)

    def __unicode__(self):
        return self.name

    def clean(self):
        self.slug = slugify(self.name)


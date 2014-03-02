from slugify import slugify
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from app.models import *

dinosaurs = Blueprint('dinosaurs', __name__, template_folder='templates')

class Search(MethodView):

  def get(self):
    name = request.args.get('name', '')

    pet_type = request.args.get('pet_type', '')


    count = Pets.objects.count()
    if request.args.get('n'):
      count = int(request.args.get('n').encode("utf8")) or Pets.objects.count()



    try:
      pets = Pets.objects.filter(name__contains=name, pet_type__contains=pet_type)
    except Pets.DoesNotExist:
      pets = []

    form_data = {'name': name,'pet_type':pet_type, 'count':count}
    if count > 0:
      return render_template('dating/pets.html', pets=pets[:count], data=form_data )
    else:
      return render_template('dating/pets.html', pets=pets, data=form_data )


class Home(MethodView):

  def get(self):
    return render_template('dating/home.html')

class ShowDinosaur(MethodView):

  def get(self, slug):
    dinosaur = Dinosaur.objects.get_or_404(slug=slug)
    return render_template('dating/show.html', dinosaur=dinosaur)


class CreateDinosaur(MethodView):

  def get(self):
    return render_template('dinosaurs/create.html')

  def post(self):

    if request.method == 'POST':
      name = request.form['name']
      dinosaur_type = request.form['type']
      height = request.form['height']
      image = request.form['image']
      slug = slugify(name)
      dinosaur = Dinosaur(name=name, dinosaur_type=dinosaur_type, height=height, image=image slug=slug)
      dinosaur.save()

      return render_template('dinosaurs/show.html', dinosaur=dinosaur)
    return render_template('dinosaurs/create.html')


dinosaurs.add_url_rule('/', view_func=Home.as_view('home'))
dinosaurs.add_url_rule('/search', view_func=Search.as_view('search'))
dinosaurs.add_url_rule('/create', view_func=CreateDinosaur.as_view('create'))
dinosaurs.add_url_rule('/dinosaur/<slug>/', view_func=ShowDinosaur.as_view('show'))



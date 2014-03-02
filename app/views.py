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
  # dinosaur  = Dinosaurs(name="t-rex", height="70m", dinosaur_type="badass", imageURL="http://1.bp.blogspot.com/-u-rpqjoaTI8/UjndjDF44OI/AAAAAAAAA4o/ty_qWLXlCuo/s1600/Dinosaurs_Lasers.jpg)")
    return render_template('dinosaurs/show.html', dinosaur=dinosaur)



dinosaurs.add_url_rule('/', view_func=Home.as_view('home'))
dinosaurs.add_url_rule('/search', view_func=Search.as_view('search'))
dinosaurs.add_url_rule('/dinosaurs/<slug>/', view_func=ShowDinosaur.as_view('show'))



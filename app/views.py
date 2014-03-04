from slugify import slugify
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from app.models import *

helpers = Blueprint('helpers', __name__, template_folder='templates')

class Search(MethodView):

  def get(self):
    name = request.args.get('name', '')

    dinosaur_type = request.args.get('type', '')

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
    helpers = Helper.objects.all()
    return render_template('helpers/home.html', helpers=helpers)

class ShowHelper(MethodView):

  def get(self, slug):
    print slug
    helpers = Helpers.objects.get_or_404(slug=slug)
  # dinosaur  = Dinosaurs(name="t-rex", height="70m", dinosaur_type="badass", imageURL="http://1.bp.blogspot.com/-u-rpqjoaTI8/UjndjDF44OI/AAAAAAAAA4o/ty_qWLXlCuo/s1600/Dinosaurs_Lasers.jpg)")
    return render_template('helpers/show.html', helpers=helpers)


class CreateHelper(MethodView):

  def get(self):
    return render_template('helpers/create.html')

  def post(self):

    if request.method == 'POST':
      name = request.form['name']
      skill = request.form['skill']
      location = request.form['location']
      slug = slugify(name)
      helper = Helper(name=name, skill=skill, location=location,slug=slug)
      helper.save()

      return render_template('helpers/show.html', helper=helper)
    return render_template('helpers/create.html')


helpers.add_url_rule('/', view_func=Home.as_view('home'))
helpers.add_url_rule('/search', view_func=Search.as_view('search'))
helpers.add_url_rule('/create', view_func=CreateHelper.as_view('create'))
helpers.add_url_rule('/helpers/<slug>/', view_func=ShowHelper.as_view('show'))



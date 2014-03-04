from slugify import slugify
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from app.models import *

helpers = Blueprint('helpers', __name__, template_folder='templates')

class Search(MethodView):

  def get(self):
    skill = request.args.get('skill','')
    location = request.args.get('location','')

    try:
      results = Helper.objects.filter(skill__contains=skill, location__contains=location)
    except Helper.DoesNotExist:
      results = []

    form_data = {'skill':skill, 'location':location }
    return render_template('helpers/search.html', results=results, data=form_data )
    


class Home(MethodView):


  def get(self):
    helpers = Helper.objects.all()
    return render_template('helpers/home.html', helpers=helpers)

class ShowHelper(MethodView):

  def get(self, slug):
    print slug
    helper = Helper.objects.get_or_404(slug=slug)
    return render_template('helpers/show.html', helper=helper)


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



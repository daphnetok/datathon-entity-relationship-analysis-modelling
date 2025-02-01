# store the standard routes for our website, ie where our users can go to
# home page, about page, etc.

from flask import Blueprint, render_template, request, flash, jsonify
import json
from .api_caller import *
from .realtimechart import create_graph

# blueprint means that it has a bunch of routes and urls inside of it
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # decorator: whenever we go to this url, itll run home()
def home():
    api_response = None
    if request.method == 'POST':
        query = request.form.get('query')
        api_response = call_api_summary(query)
        entities_relationships = call_api_entities(query)
        graph_img = create_graph(entities_relationships)

        if api_response:
            flash('Successful!', category='success')
        else:
            flash('Failed. Try again.', category='error')

        return render_template("answer.html", api_response = api_response, graph_img = graph_img, entities_relationships = entities_relationships) # renders the html in home.html, reference the current user in our template and check if it is authenticated
    return render_template("query.html")

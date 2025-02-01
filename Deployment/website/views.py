# store the standard routes for our website, ie where our users can go to
# home page, about page, etc.

from flask import Blueprint, render_template, request, flash, jsonify
import json
from .api_caller import *
from .realtimechart import create_graph
import asyncio

# blueprint means that it has a bunch of routes and urls inside of it
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # decorator: whenever we go to this url, itll run home()
def home():
    if request.method == 'POST':
        query = request.form.get('query')

        # Ensure we run the async functions properly within Flask
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        api_response, entities_relationships = loop.run_until_complete(
            asyncio.gather(call_api_summary(query), call_api_entities(query))
        )

        graph_img = create_graph(entities_relationships)

        if api_response:
            flash('Successful!', category='success')
        else:
            flash('Failed. Try again.', category='error')

        return render_template("answer.html", api_response = api_response, graph_img = graph_img, entities_relationships = entities_relationships) # renders the html in home.html, reference the current user in our template and check if it is authenticated
    return render_template("query.html")

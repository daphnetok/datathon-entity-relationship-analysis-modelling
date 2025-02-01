from flask import Blueprint, render_template, request, flash, jsonify
import json
from .api_caller import *
from .realtimechart import create_graph
from .model import classifier
import asyncio

# blueprint means that it has a bunch of routes and urls inside of it
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # decorator: whenever we go to this url, itll run home()
def home():
    if request.method == 'POST':
        query = request.form.get('query')

        # Handle empty query input
        if not query:
            flash('Query cannot be empty.', category='error')
            return render_template("query.html")

        try:
            query = request.form.get('query')
            api_response = call_api_summary(query)
            entities_relationships = call_api_entities(query)
            graph_img = create_graph(entities_relationships)

            # Classify the user input using the ML model
            classification_label = classifier(query)

            if api_response:
                flash('Successful!', category='success')
            else:
                flash('Failed. Try again.', category='error')

            return render_template("answer.html", 
                                    api_response = api_response, 
                                    graph_img = graph_img, 
                                    entities_relationships = entities_relationships,
                                    classification_label = classification_label)
        
        except Exception as e:
            # Log the error and display an error message
            print(f"Error: {e}")
            flash('An error occurred while processing your request.', category='error')
            return render_template("query.html")

    return render_template("query.html")

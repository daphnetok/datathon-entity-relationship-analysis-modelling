import requests
import json
import pandas as pd
import os

def call_api_entities(text):
    # API endpoint
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    # Define the API payload
    data = {
        "model": "llama3.2",
        "prompt": f"""Identify the entities and the relationship between entities in the following text.
        '{text}'
        Give me the response in this format. Give me as many entities and their relationships as possible. 
        **Entities:**
            1. (Entity) - (Description)

        **Relationships:**
            1. (Entity) has relationships with:
                * (Another Entity) - Relationship between Entities
                * (Another Entity) - Relationship between Entities
            
        For example, when given the text '
        'Starbucks violated federal labor law when it increased wages and offered new perks and benefits only to non-union employees, a National Labor Relations Board judge found Thursday.

        The decision is the latest in a series of NLRB rulings finding that Starbucks has violated labor law in its efforts to stop unions from forming in its coffee shops.

        “The issue at the heart of this case is whether, under current Board law, [Starbucks] was entitled to explicitly reward employees,” for not participating in union activity, “while falsely telling its workers that the federal labor law forced it to take this action,” wrote administrative law judge Mara-Louise Anzalone. “It was not.”'
        ', give me the following response. 
        **Entities:**

            1. Starbucks - Coffee shop chain company
            2. National Labor Relations Board (NLRB) - Government agency responsible for enforcing federal labor laws
            3. Mara-Louise Anzalone - Administrative law judge at NLRB
            4. Federal labor law - Law governing employment practices in the United States

        **Relationships:**

            1. Starbucks has relationships with:
                * National Labor Relations Board (NLRB) - Starbucks was found to have violated labor laws enforced by the NLRB.
                * Mara-Louise Anzalone - As an administrative law judge at NLRB, she made the ruling in this case.
            2. National Labor Relations Board (NLRB) has relationships with:
                * Federal labor law - The NLRB enforces federal labor laws and makes rulings on cases involving violations of these laws.
            3. Mara-Louise Anzalone has relationships with:
                * National Labor Relations Board (NLRB) - As an administrative law judge, she is employed by the NLRB and works within its jurisdiction.
            4. Federal labor law has relationships with:
                * Starbucks - The law applies to employment practices in Starbucks' coffee shops, as seen in this case.
                * National Labor Relations Board (NLRB) - The law is enforced by the NLRB, which made the ruling in this case.
            """,
        "stream": False
    }

    # Make API request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        actual_response = response.json().get("response", "No response")
        print("we got response")
    except requests.exceptions.RequestException as e:
        actual_response = f"API Error: {str(e)}"
        print(f"API Error: {str(e)}")
        
    return actual_response

def call_api_summary(text):
    # API endpoint
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    # Define the API payload
    data = {
        "model": "llama3.2",
        "prompt": f"""Summarise the following text in one sentence.
        '{text}'""",
        "stream": False
    }

    # Make API request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        actual_response = response.json().get("response", "No response")
        print("we got response")
    except requests.exceptions.RequestException as e:
        actual_response = f"API Error: {str(e)}"
        print(f"API Error: {str(e)}")
        
    return actual_response


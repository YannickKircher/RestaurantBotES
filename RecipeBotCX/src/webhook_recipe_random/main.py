import pymongo
import numpy as np
from datetime import datetime
from google.cloud import bigquery
from configparser import ConfigParser
from json_return import json_recipe_data, json_text_response
from big_query_templates import history_add_new_entry, history_delete_old_entries

def main(request):

    request_json = request.get_json(silent=True)

    #read mogodb password from config file
    config = ConfigParser()
    config.read("secrets_recipe_bot.ini")
    MONGO_DB_PW = config["SECRETS"]["MONGO_DB_PW"]

    # mongo db init
    mongo_client = pymongo.MongoClient(f"mongodb+srv://kircheryannick:{MONGO_DB_PW}@cluster0.fvwxqpp.mongodb.net/?retryWrites=true&w=majority")
    recipes_collection = mongo_client["chatbot"]["recipes"]

    # mongo db query
    recipe_id = request_json["sessionInfo"]["parameters"].get("recipe_id",None)
    
    #find relevant recipes
    recipes = [x for x in recipes_collection.aggregate([{ "$sample": { "size": 1 } }])]

    #No recipe found
    if len(recipes) == 0:
        return json_text_response("No recipe found") 

    else:
        recipe = recipes[0]
        
    print(recipe)
    #Response
    into_message = ""
    recipe_id = str(recipe["_id"])
    recipe_name = recipe["title"]
    recipe_ingredients = recipe["ingredients"]
    recipe_instructions = recipe["directions"]
    
    #manage history
    client = bigquery.Client()
    db_table_to_query = "`dialogflow-recipe-guide.chatbot.user_recipe_history`"
    
    history_add_new_entry(client,
                          db_table_to_query,
                          recipe_id,
                          recipe_name,
                          "example_user_id",
                          datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    history_delete_old_entries(client,
                                db_table_to_query,
                               "example_user_id")
    
    #response
    response = json_recipe_data(recipe_id,
                            into_message,
                            recipe_name,
                            recipe_ingredients,
                            recipe_instructions
                            )
    print(response)
    return response
import pymongo
import numpy as np
from configparser import ConfigParser
from json_return import json_recipe_data, json_text_response

def main(request):

    request_json = request.get_json(silent=True)
    print(request_json)

    config = ConfigParser()
    config.read("secrets_recipe_bot.ini")
    MONGO_DB_PW = config["SECRETS"]["MONGO_DB_PW"]

    QUERY_LIMIT = 100

    # mongo db init
    mongo_client = pymongo.MongoClient(f"mongodb+srv://kircheryannick:{MONGO_DB_PW}@cluster0.fvwxqpp.mongodb.net/?retryWrites=true&w=majority")
    recipes_collection = mongo_client["chatbot"]["recipes"]

    # mongo db query
    recipe_name = request_json["sessionInfo"]["parameters"]["recipe"]
    
    recipe_id = request_json["sessionInfo"]["parameters"].get("recipe_id",None)
    print("start",recipe_id)
    
    recipes = [x for x in recipes_collection.find({"title": {"$regex" : recipe_name, "$options" : "i"}}).limit(QUERY_LIMIT)]

    #No recipe found
    if len(recipes) == 0:
        return json_text_response("No recipe found")

    #reroll if recipe_id is already in recipes
    elif len(recipes) == 1:
        recipe = recipes[0]
        into_message = "I found one recipe"
    #get random recipe
    else:
        recipe = np.random.choice(recipes)
        into_message = f"I found {len(recipes)} recipes"

    #Response
    recipe_id = str(recipe["_id"])
    recipe_name = recipe["title"]
    recipe_ingredients = recipe["ingredients"]
    recipe_instructions = recipe["directions"]
    
    print("end",recipe_id)
    response = json_recipe_data(recipe_id,into_message,recipe_name,recipe_ingredients,recipe_instructions)
    return response
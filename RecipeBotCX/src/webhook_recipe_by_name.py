import pymongo
from configparser import ConfigParser
from json_return import json_recipe_data

def main(request):

    request_json = request.get_json(silent=True)
    print(request_json)

    #intent = request_json["queryResult"]["intent"]

    config = ConfigParser()
    config.read("secrets_recipe_bot.ini")
    MONGO_DB_PW = config["SECRETS"]["MONGO_DB_PW"]

    QUERY_LIMIT = 1

    # mongo db init
    mongo_client = pymongo.MongoClient(f"mongodb+srv://kircheryannick:{MONGO_DB_PW}@cluster0.fvwxqpp.mongodb.net/?retryWrites=true&w=majority")
    recipes_collection = mongo_client["chatbot"]["recipes"]

    recipe_name = request_json["sessionInfo"]["parameters"]["recipe"]
    recipes = [x for x in recipes_collection.find({"title": {"$regex" : recipe_name, "$options" : "i"}}).limit(QUERY_LIMIT)]

    
    recipe_id = str(recipes[0]["_id"])
    recipe_name = recipes[0]["title"]
    recipe_ingredients = recipes[0]["ingredients"]
    recipe_instructions = recipes[0]["directions"]
    
    print(
        recipe_id,
        recipe_name,
        recipe_ingredients,
        recipe_instructions
    )
    
    response = json_recipe_data(recipe_id,recipe_name,recipe_ingredients,recipe_instructions)
    print(response)
    
    return response
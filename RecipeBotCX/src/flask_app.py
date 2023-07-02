from flask import Flask, jsonify, request

import pymongo
from configparser import ConfigParser

# config
config = ConfigParser()
config.read("/home/lemmy/Workspace/dialogflowchatbot/SECRETS/secrets_recipe_bot.ini")
MONGO_DB_PW = config["SECRETS"]["MONGO_DB_PW"]

# mongo db init
mongo_client = pymongo.MongoClient(f"mongodb+srv://kircheryannick:{MONGO_DB_PW}@cluster0.fvwxqpp.mongodb.net/?retryWrites=true&w=majority")
recipes_collection = mongo_client["chatbot"]["recipes"]

# flask app init 
app = Flask(__name__)

# Get all books
@app.route('/name', methods=['GET'])
def get_books(request):
    print(request)
    return request.get_json()#jsonify(recipe_name_intent_handler(recipes_collection,name = "COOKIES"))

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
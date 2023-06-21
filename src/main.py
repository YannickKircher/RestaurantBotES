from pandas import DataFrame
from google.cloud import bigquery
from json_return import return_text, return_card
from query import CustomQuery
from intenthandler import restaurant_intent_handler

def webhook_call(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    
    intent = request_json["queryResult"]["intent"]["displayName"]
    
    if intent == "restaurants":
        return restaurant_intent_handler(request_json)

    else:
        return None

    
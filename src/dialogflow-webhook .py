import numpy as np
from google.cloud import bigquery


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
    #print(request_json)
    
    intent = request_json["queryResult"]["intent"]["displayName"]

    random_id = np.random.randint(0,48)

    query = f"SELECT * FROM `restaurantguide-9oyv.restaurant_guide.restaurants` WHERE int64_field_0 = {random_id}"

    client = bigquery.Client()
    query_job = client.query(query)

    for r in query_job:
        row = r
        break

    # response = {
    #         "fulfillmentMessages": [
    #             {
    #             "text": {
    #                 "text": [
    #                 f"Text response from webhook with intent: {intent}"
    #                 ]
    #             }
    #             }
    #         ]
    # }   
    
    response = {
        "fulfillmentMessages": [
            {
            "card": {
                "title": row["name"],
                "subtitle": row["Rating"],
                "imageUri": row["img_url"],
            }
            }
        ]
        }
    return response



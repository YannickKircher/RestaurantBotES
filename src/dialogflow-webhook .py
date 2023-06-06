import json

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
    print(request_json)
    
    intent = request_json["queryResult"]["intent"]["displayName"]

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
                "title": f"you tried to execute: {intent}",
                "subtitle": "card text",
                "imageUri": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/22/a1/3d/89/aerial-view.jpg?w=1000&h=600&s=1",
            }
            }
        ]
        }
    return response



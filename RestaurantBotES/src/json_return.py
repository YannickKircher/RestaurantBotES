
def return_card(title,subtitle,img_url,btn_url=None,btn_text=None):
    """builds a json response with a card response, 
    that includes a img and a button,
    that can be shown by the dialogflow API to the user"""
    if (btn_url is not None) & (btn_text is not None): 
        return {
            "fulfillmentMessages": [
                {
                "card": {
                    "title": title,
                    "subtitle": subtitle,
                    "imageUri": img_url,
                    "buttons": [
                    {
                        "text": btn_text,
                        "postback": btn_url
                    }
                    ]
                }
                }
            ]
            }
    else:
        return {
            "fulfillmentMessages": [
                {
                "card": {
                    "title": title,
                    "subtitle": subtitle,
                    "imageUri": img_url,
                }
                }
            ]
            }

def return_text(text_response):
    """builds a json response with a text response, 
    that can be shown by the dialogflow API to the user"""
    return {
        "fulfillmentMessages": [
            {
            "text": {
                "text": [
                text_response
                ]
            }
            }
        ]
        }

def return_text_test(text_response,):
    """builds a json response with a text response, 
    that can be shown by the dialogflow API to the user"""
    return {
        "fulfillmentMessages": [
            {
            "text": {
                "text": [
                text_response
                ]
            }
            }
        ],
        "sessionInfo": [
            {
                "parameters": {
                    "restaurant": "123",
                }
            }
        ],
    }
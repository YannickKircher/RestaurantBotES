def return_card(title,subtitle,img_url,btn_url=None,btn_text=None):
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


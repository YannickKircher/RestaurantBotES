from pandas import DataFrame
from google.cloud import bigquery

default_user_price_range = "low"

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
    

def restaurant_intent_handler(request_json):
    client = bigquery.Client()
    print(request_json["queryResult"]["parameters"])
    try:
        query = CustomQuery(table_name="`restaurantguide-9oyv.restaurant_guide.restaurants_random`")
        #check for price preference and add a where statement if found
        if request_json["queryResult"]["parameters"]["price_range"] != "None":
            query.add_where({f'price_range' : f'= "{request_json["queryResult"]["parameters"]["price_range"].lower()}"'})
        
        #check for cuisin preference and add a where statement if found
        if request_json["queryResult"]["parameters"]["cuisine"] != "None":
            query.add_where({'country': f' = "{request_json["queryResult"]["parameters"]["cuisine"].lower()}"'})
    
        query.limit = 4
        query_job = client.query(str(query))
        query.clear()
        query_df = DataFrame([dict(row) for row in query_job])
        
        return return_card(title = query_df["name"][0],
                       subtitle = str([round(query_df["rating"][0],2), query_df["country"][0], query_df["price_range"][0]]),
                       img_url = query_df["img_url"][0],
                       btn_url = query_df["img_url"][0],
                       btn_text = "go to Restaurant web page"
                       )
        
    except KeyError:
        global default_user_price_range
        query = CustomQuery(table_name="`restaurantguide-9oyv.restaurant_guide.restaurants_random`",
                            where_statements={'price_range':f'= "{default_user_price_range}"'},
                            order_by_list=["rating"], limit=10)
    
        query_job = client.query(str(query))

        query_df = DataFrame([dict(row) for row in query_job])
        sample_df = query_df.sample()
        
        return return_card(title = sample_df["name"].values[0],
                        subtitle = "I could not find any sprecific restaurant, but you might like this" 
                                        + str([sample_df["rating"].values[0], sample_df["country"].values[0], sample_df["price_range"].values[0]]),
                        img_url = sample_df["img_url"].values[0],
                        btn_url = sample_df["img_url"].values[0],
                        btn_text = "go to Restaurant web page"
                        )


class CustomQuery():
    def __init__(self, table_name:str, column_names_to_select:str="*", where_statements:dict={}, order_by_list:list=[], order_desc:bool=True, limit:int=None):
        self.column_names_to_select = column_names_to_select
        self.table_name = table_name
        self._where_statements = where_statements
        self.order_by_list = order_by_list
        self.order_desc = order_desc
        self.limit = limit
    
    def add_where(self,where_statements:dict):
        """append a WHERE statement to query, like:
           {"rating":">= 10", "test":"='test2'"}
        """
        
        self._where_statements.update(where_statements)
    
    def clear(self):
        self._where_statements={}
        
    def __str__(self):
        """builds the final query and returns it as a str"""
        basic_query_str = f"SELECT {self.column_names_to_select} FROM {self.table_name}"
        
        if len(self._where_statements) > 0:
            basic_query_str += " WHERE "
            basic_query_str += " AND ".join([f"{key} {value}" for key,value in self._where_statements.items()])
        
        if len(self.order_by_list) > 0:
            basic_query_str+= " ORDER BY "+", ".join(self.order_by_list)
            if self.order_desc:
                basic_query_str+= " DESC"
            else:
                basic_query_str+= " ASC"
            
        if self.limit is not None:
            basic_query_str+= f" LIMIT {self.limit}"
            
        return basic_query_str
    

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


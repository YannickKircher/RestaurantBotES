from pandas import DataFrame
from google.cloud import bigquery
from json_return import return_text, return_card
from query import CustomQuery

default_user_price_range = "low"

def restaurant_intent_handler(request_json):
    client = bigquery.Client()
    
    if len(request_json["queryResult"]["parameters"]["dish"]) > 0 :
        query = "SELECT * FROM `restaurantguide-9oyv.restaurant_guide.restaurants_random` ORDER BY rating DESC"
        query_job = client.query(query)
        query_df = DataFrame([dict(row) for row in query_job])
        
        print("QDF:  ",query_df, query_df.shape)
        
        #if query_df
        
        
        #select first (best rated) restaurant with the dish on the menu
        # workaround because I'm not using NoSQL 
        for dish in request_json["queryResult"]["parameters"]["dish"]:
            restaurant = [item for item in query_df.iterrows() if dish in item[1]["menu_list"]][0][1]
            break
        
        return return_card(title = restaurant["name"],
                            subtitle = str([round(restaurant["rating"],2), restaurant["country"], restaurant["price_range"]]),
                            img_url = restaurant["img_url"],
                            btn_url = restaurant["img_url"],
                            btn_text = "go to Restaurant web page"
                            )
        
    else:
        try:
            query = CustomQuery(table_name="`restaurantguide-9oyv.restaurant_guide.restaurants_random`",order_by_list=["rating"])
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
            sample_df = query_df.sample()
            

            return return_card(title = sample_df["name"].values[0],
                            subtitle = str([round(sample_df["rating"].values[0],2), sample_df["country"].values[0], sample_df["price_range"].values[0]]),
                            img_url = sample_df["img_url"].values[0],
                            btn_url = sample_df["img_url"].values[0],
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
                                            + str([round(sample_df["rating"].values[0],2), sample_df["country"].values[0], sample_df["price_range"].values[0]]),
                            img_url = sample_df["img_url"].values[0],
                            btn_url = sample_df["img_url"].values[0],
                            btn_text = "go to Restaurant web page"
                            )

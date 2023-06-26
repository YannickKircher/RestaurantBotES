from pandas import DataFrame
from google.cloud import bigquery
from json_return import return_text, return_card
from query import CustomQuery


def restaurant_intent_handler(request_json):
    
    #default user preferences for simulating a generic user
    #-> because i dont have user accounts
    default_user_price_range = "low"
    default_user_location = "Matera"
    default_user_openness = 4 
    
    db_table_to_query = "`restaurantguide-9oyv.restaurant_guide.restaurants_random`"
    
    
    client = bigquery.Client()
 
    # if a dish was given as a parameter, return the best rated restaurant with that dish on the menu and a matching location
    if len(request_json["queryResult"]["parameters"]["dish"]) > 0 :
        query = CustomQuery(table_name=db_table_to_query,order_by_list=["rating"])
        #check for location preference and add a where statement if found
        if request_json["queryResult"]["parameters"]["geo-city"] != "None":
            query.add_where({'location': 
                f' = "{request_json["queryResult"]["parameters"]["geo-city"]}"'})
        
        query_job = client.query(str(query))
        #query.clear()
        query_df = DataFrame([dict(row) for row in query_job])
        
        
        #select first (best rated) restaurant with the dish on the menu
        # WORKAROUND BECAUSE I AM NOT USING NoSQL <--------
        for dish in request_json["queryResult"]["parameters"]["dish"]:
            restaurant_list = [item for item in query_df.iterrows() 
                                if dish in item[1]["menu_list"] or dish.capitalize() 
                                in item[1]["menu_list"]]
            break
        
        #found no restaurant with that item on the menu 
        if len(restaurant_list) == 0:
            return return_text(
                f"""I'm sorry, I could not find any Restaurant with the dishes {
                    ', '.join(request_json["queryResult"]["parameters"]["dish"])
                    } on the Menu""")

        else: #found at least 1 -> pick the best rated one
            restaurant = restaurant_list[0][1]
            return return_card(title = restaurant["name"],
                                subtitle = str([
                                        round(restaurant["rating"],2), 
                                        restaurant["country"], 
                                        restaurant["price_range"], 
                                        restaurant["location"],
                                        restaurant["menu_list"],
                                    ]),
                                img_url = restaurant["img_url"],
                                btn_url = restaurant["img_url"],
                                btn_text = "go to Restaurant web page"
                                )
    
    # query for a restaurant with the given parameters except for the dishes
    else:
        try: 
            query = CustomQuery(table_name=db_table_to_query,order_by_list=["rating"])
            #check for price preference and add a where statement if found
            if request_json["queryResult"]["parameters"]["price_range"] != "None":
                query.add_where({f'price_range' :
                    f'= "{request_json["queryResult"]["parameters"]["price_range"].lower()}"'})
            
            #check for cuisine preference and add a where statement if found
            if request_json["queryResult"]["parameters"]["cuisine"] != "None":
                query.add_where({'country':
                    f' = "{request_json["queryResult"]["parameters"]["cuisine"].lower()}"'})
                
            #check for location preference and add a where statement if found
            if request_json["queryResult"]["parameters"]["geo-city"] != "None":
                query.add_where({'location':
                    f' = "{request_json["queryResult"]["parameters"]["geo-city"]}"'})
            else:
                query.add_where({'location': f' = "{default_user_location}"'})

            #pick a random restaurant from the top n restaurants
            #n is equal to the user openness
            query.limit = default_user_openness
            
            #query
            print(str(query))
            query_job = client.query(str(query))
            #query.clear()
            query_df = DataFrame([dict(row) for row in query_job])
            
            #pick on of the top n restaurants
            sample_df = query_df.sample()
            

            return return_card(title = sample_df["name"].values[0],
                            subtitle = str([round(sample_df["rating"].values[0],2),
                                            sample_df["country"].values[0],
                                            sample_df["price_range"].values[0],
                                            sample_df["location"].values[0]]),
                            img_url = sample_df["img_url"].values[0],
                            btn_url = sample_df["img_url"].values[0],
                            btn_text = "go to Restaurant web page"
                            )
        
        # if the query returns no valid restaurant that fits the specifications, 
        # -> return a restaurant, that matches default user preferences 
        # and the location if given else use default_user_location
        except KeyError:
            query = CustomQuery(table_name=db_table_to_query,
                                where_statements={'price_range':f'= "{default_user_price_range}"'},
                                order_by_list=["rating"], limit = default_user_openness)
            if request_json["queryResult"]["parameters"]["geo-city"] != "None":
                query.add_where({'location':
                    f' = "{request_json["queryResult"]["parameters"]["geo-city"]}"'})
            else:
                query.add_where({'location': f' = "{default_user_location}"'})
        
            #query
            query_job = client.query(str(query))
            query_df = DataFrame([dict(row) for row in query_job])
            sample_df = query_df.sample()
            
            return return_card(title = sample_df["name"].values[0],
                            subtitle = "I could not find any sprecific restaurant, but you might like this" 
                                            + str([round(sample_df["rating"].values[0],2),
                                                   sample_df["country"].values[0],
                                                   sample_df["price_range"].values[0],
                                                   sample_df["location"].values[0]]),
                            img_url = sample_df["img_url"].values[0],
                            btn_url = sample_df["img_url"].values[0],
                            btn_text = "go to Restaurant web page"
                            )

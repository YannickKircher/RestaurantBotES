def rich_text(texts:list,content_type="chips"):
    return {
            "richContent": [
                [
                    {
                        "options": [{"text": text} for text in texts],
                        "type": content_type
                    }
                ]
            ]
        }


def json_recipe_data(recipe_id,into_message,recipe_name,ingredients,directions):
  
  lines = [into_message]+[recipe_name]+["\n".join(["Ingredients:"]+ingredients)]+["\n".join(["Directions:"]+directions)]
  
  return {
   "fulfillment_response": {
     "messages": [
       {
         "text": {
           "text": [line]
         }
       } for line in lines 
     ]
   },
   "sessionInfo": {
     "parameters": {
          "recipe_id": recipe_id
     }
   }
 }
  

def json_text_response(text):
  
  
  return {
   "fulfillment_response": {
     "messages": [
       {
         "text": {
           "text": [text]
         }
       } 
     ]
   },
   "sessionInfo": {
     "parameters": {
          "recipe_id": None
     }
   }
 }
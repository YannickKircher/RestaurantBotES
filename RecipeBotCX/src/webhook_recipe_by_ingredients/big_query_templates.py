def history_add_new_entry(client,db_table_to_query,recipe_id,recipe_name,user_id,timestamp):
    insert_query = f"""
            insert
            into {db_table_to_query}
            values("{recipe_id}","{recipe_name}","{user_id}", "{timestamp}")"""
    return client.query(insert_query)

def history_delete_old_entries(client,db_table_to_query,user_id):
    delete_query = f"""
            delete 
            from {db_table_to_query}
            where (user_id = "{user_id}") and entry_added < (
                select entry_added 
                from {db_table_to_query} 
                where user_id = "{user_id}"
                order by entry_added desc 
                limit 1 
                offset 3 
            )"""
    return client.query(delete_query)
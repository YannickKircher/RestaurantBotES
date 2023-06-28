
class CustomQuery():
    def __init__(self, table_name:str,
                 column_names_to_select:str="*",
                 where_statements:dict=None,
                 order_by_list:list[str]=None,
                 order_desc:bool=True,
                 limit:int=None):
        """CustomQuery class to build a SQL query.

        Args:
            table_name (str): table to query from
            column_names_to_select (str, optional): column names to select. Defaults to "*".
            where_statements (dict, optional): where statements like: 
                {"rating":">= 10", "test":"='test2'"}. 
                Defaults to None.
            order_by_list (list, optional): columns to order the results by. Defaults to None.
            order_desc (bool, optional): how to order all the columns. Defaults to True.
            limit (int, optional): limit of selections. Defaults to None.
        """
        
        if where_statements is None:
            self._where_statements = {}
        else:
            self._where_statements = where_statements
            
        if order_by_list is None:
            self.order_by_list = []
        else:
            self.order_by_list = order_by_list
            
        
        self.column_names_to_select = column_names_to_select
        self.table_name = table_name
        self.order_desc = order_desc
        self.limit = limit
    
    def add_where(self,where_statements:dict):
        """append a WHERE statement to query, like:
           {"rating":">= 10", "test":"='test2'"}
        """
        
        self._where_statements.update(where_statements)
    
    def clear(self):
        self._where_statements={}
        self.order_by_list=[]
        
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
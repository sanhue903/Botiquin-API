from app.extensions import db

from flask import request

def filter_query(query, model_type, atribute : str, filter: str):
    if filter.isdecimal():
    
        equal = request.args.get(filter, None, type=int)
        low_bound = request.args.get(f'{filter}[gte]', None, type=int)
        high_bound = request.args.get(f'{filter}[lte]', None, type=int)
            
        if low_bound is not None:
            query = query.where(getattr(model_type, atribute) >= low_bound)
    
        if high_bound is not None:
            query = query.where(getattr(model_type, atribute) <= high_bound)
        
    else:
        equal = request.args.get(filter, None, type=str)

    if equal is not None:
        query = query.where(getattr(model_type, atribute) == equal) 

    return query

def get_items_from_query(query):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    
    return db.paginate(query, page=page, per_page=limit,max_per_page=None, error_out=False).items
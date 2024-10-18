from flask import request
from app.extensions import db

def filter_query(query, model_type, filter : str):
    equal = request.args.get(filter, None, type=int)
    low_bound = request.args.get(f'{filter}[gte]', None, type=int)
    high_bound = request.args.get(f'{filter}[lte]', None, type=int)
    
    if equal is not None:
        query = query.where(getattr(model_type, filter) == equal) 
    
    if low_bound is not None:
        query = query.where(getattr(model_type, filter) >= low_bound)
    
    if high_bound is not None:
        query = query.where(getattr(model_type, filter) <= high_bound)
    
    return query

def get_items_from_query(query):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    
    return db.paginate(query, page=page, per_page=limit,max_per_page=None, error_out=False).items
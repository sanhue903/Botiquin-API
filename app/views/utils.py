from app.extensions import db

from flask import request

def filter_query(query, model_type, attribute, value, filter_type='equal'):
    if value is not None:
        if filter_type == 'gte':
            query = query.where(getattr(model_type, attribute) >= value)
        elif filter_type == 'lte':
            query = query.where(getattr(model_type, attribute) <= value)
        elif filter_type == 'equal':
            query = query.where(getattr(model_type, attribute) == value) 
    
    return query
        

def get_less_equal_greater_filters(query, model_type, attribute : str):
    equal = request.args.get(attribute, None, type=int)
    low_bound = request.args.get(f'{attribute}[gte]', None, type=int)
    high_bound = request.args.get(f'{attribute}[lte]', None, type=int)
            
    query = filter_query(query, model_type, attribute, equal)
    query = filter_query(query, model_type, attribute, low_bound, 'gte')
    query = filter_query(query, model_type, attribute, high_bound, 'lte')


    return query

def get_items_from_query(query):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    
    return db.paginate(query, page=page, per_page=limit,max_per_page=None, error_out=False).items
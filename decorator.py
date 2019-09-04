
def log2mongo(func):
    def wrapper(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        # log something here to MongoDB
        print(f'>>> pushing {returned_value} to MongoDB')
        return returned_value
    return wrapper

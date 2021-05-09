from games_of_data.settings import database

def execute_aggregation(colleciton_name: str, aggregate: list):
    collection = database[colleciton_name]
    return list(collection.aggregate(aggregate))

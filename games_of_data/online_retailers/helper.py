result = []


def filter_by_ram(data_of_document: list):
    result = []
    for document in data_of_document:
        try:
            if isinstance(document["_id"]["ram"], int) and 32 > document["_id"]["ram"] >= 2:
                result.append({"company": document["_id"]["company"],
                               "RAM": document["_id"]["ram"],
                               "Avg_price": round(document["sum"] / document["count"], 4)})

        except KeyError:
            pass
    return result
def normalize_path_params(city=None,min_stars = 0,max_stars = 5,min_price = 0,max_price = 1000,limit=50,offset=0,**data):
    if city:
        return {
            "min_stars":min_stars,
            "max_stars":max_stars,
            "min_price":min_price,
            "max_price":max_price,
            "city":city,
            "limit":limit,
            "offset":offset
        }
    
    return {
            "min_stars":min_stars,
            "max_stars":max_stars,
            "min_price":min_price,
            "max_price":max_price,
            "limit":limit,
            "offset":offset
        }

query_if_not_city =  "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?)\
            and (price >= ? and price <= ?) LIMIT ? OFFSET ?"

query_if_city = "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?)\
                and (price >= ? and price <= ?) and city = ? LIMIT ? OFFSET ? "
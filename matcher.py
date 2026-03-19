from geocoder import get_proximity_score #imports the function from geocoder

def calculate_match_score(property, preferences): #takes one property and one set of tenant preferences , returns the score out of 100
    score = 0
    #City match - 15 points
    city_matched = False  #flag starts as False
    if property["city"].lower() == preferences["city"].lower():
        score +=15
        city_matched = True
    
    #Area / proximity - 20 points
    if city_matched:
        proximity_score = get_proximity_score(  #calls the geocoder's function to get city and area of tenant preference and availability
            preferences.get("area",""),
            preferences["city"],
            property["area"],
            property["city"]
        )
        score += proximity_score
    
    #Budget fit - 25 points
    if property["price"] <= preferences["max_budget"]:
        score +=25
    elif property["price"] <= preferences["max_budget"] * 1.1:
        score +=10

    #BHK match - 20 points
    if property["bedrooms"] == preferences["bedrooms"]:
        score +=20 #exact match means 20 points
    elif abs(property["bedrooms"] - preferences["bedrooms"]) == 1:
        score +=8 #one bedroom difference means 8 points

    
    #Extras
    #Furnishing match - 12 points
    if property["furnishing_type"] == preferences.get("furnishing_type",""):
        score +=12
    elif property["furnishing_type"] == "semi-furnished" and preferences.get("furnishing_type") == "unfurnished":
        score += 5
    elif property["furnishing_type"] == "semi-furnished" and preferences.get("furnishing_type") == "furnished":
        score += 5
    
    #Has lift - 4 points
    if preferences.get("has_lift") == 1 and property["has_lift"] == 1:
        score += 4
    
    #Has parking - 4 points
    if preferences.get("has_parking") == 1 and property["has_parking"] == 1:
        score +=4

    return round(score)


def get_matches(properties, preferences):
    results =[]

    for property in properties:
        score = calculate_match_score(property, preferences) #loop through and find property score
        results.append({
            "property":property,
            "score": score
        })
    results.sort(key=lambda x:x["score"],reverse=True) #highest score first
    return results
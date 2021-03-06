from flask import redirect


def create_drink_list(data):
    drink_list = []
    idx = 0
    for drink in data["drinks"]:
        drink_dict = {'name': data["drinks"][idx]['strDrink'],
                      'id': data["drinks"][idx]['idDrink'],
                      'img_url' : data["drinks"][idx]['strDrinkThumb']
          }
        idx +=1
        drink_list.append(drink_dict)
    return drink_list

def create_drink_showcase(data):
    drink_list = []
    idx = 0
    for drink in range(0,6):
        drink_dict = {'name': data["drinks"][idx]['strDrink'],
                      'id': data["drinks"][idx]['idDrink'],
                      'img_url' : data["drinks"][idx]['strDrinkThumb']
          }
        idx +=1
        drink_list.append(drink_dict)
    return drink_list

def create_drink_list_by_ingredient(data):
    drink_list = []
    idx = 0
    for drink in data["drinks"]:
        drink_dict = {'name': data["drinks"][idx]['strDrink'],
                      'id': data["drinks"][idx]['idDrink'],
                      'img_url' : data["drinks"][idx]['strDrinkThumb']
          }
        idx +=1
        drink_list.append(drink_dict)
    return drink_list

def create_empty_drink():
    """Used to return a drink incase of error"""
    return {'name': "No Results Found",
                      'id': "No Results Found",
                      'img_url' : "No Results Found"}

def create_drink(data):
    ingredients = []
    measurments = []
    for i in range (1,15):
        if data["drinks"][0][f'strIngredient{i}'] is not None:
            ingredients.append( data["drinks"][0][f'strIngredient{i}'])
        if data["drinks"][0][f'strMeasure{i}'] is not None:
            measurments.append( data["drinks"][0][f'strMeasure{i}'])
    drink_dict = {'name': data["drinks"][0]['strDrink'],
                      'id': data["drinks"][0]['idDrink'],
                      'img_url' : data["drinks"][0]['strDrinkThumb'],
                      'instructions' : data["drinks"][0]['strInstructions'],
                      'ingredients' : ingredients,
                      'measurments' : measurments
          }
    return drink_dict




def create_comments(id,username, text,post_id):
    return {'user_id': id,
        'post_id':post_id,
        'username': username,
    'text': text
    }
    
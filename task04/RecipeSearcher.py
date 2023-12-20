import json, requests

# bc29c01c4c2b478ea4a4dcdbc26908e2
class Recipes:
    def __init__(self):
        pass

    def authenticate(self, apiKey):
        url = f"https://api.spoonacular.com/recipes/716429/information?apiKey={apiKey}&includeNutrition=true"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response)
            recipesFound = [recipe["title"] for recipe in response]
            return recipesFound
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def getResponse(self,ingredients, numOfRecipes, rank):
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number={numOfRecipes}&ranking={rank}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            responseContent = response.content.decode('utf-8')
            responseJson = json.loads(responseContent)
            recipesFound = [recipe["title"] for recipe in responseJson]
            return recipesFound
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

def getParameters():
    response = None
    ingredients = []
    count = 0
    while True:
        ingredient = input("\nEnter the ingredient: ").lower().strip()
        if count == 0:
            ingredients.append(f"{ingredient}")
        else:
            ingredients.append(f"+{ingredient}")

        while True:
            try:
                response = input("\nDo you wish to add another ingredient? (y/n): ").lower()
                if response in ['y', 'n']:
                    break
            except:
                print("\nPlease input either yes or no:")

        if response == 'n':
            break

    numOfRecipesRequired = int(input("\nEnter the number of recipes you need (max: 100): "))

    rank = int(input("""
            Press 1 to maximize available ingredients
            Press 2 to minimize missing ingredients: """))

    return ingredients, numOfRecipesRequired, rank


def main():
    recipes = Recipes()
    print("\nWelcome to Kartik's Recipe Finder!")

    apiKey = input("\nEnter the API Key:(bc29c01c4c2b478ea4a4dcdbc26908e2): ")
    recipes.authenticate(apiKey)

    #ingredients, numOfRecipes, rank = getParameters()
    #print(recipes.getResponse(ingredients, numOfRecipes, rank))


if __name__ == '__main__':
    main()
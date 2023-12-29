import json, requests


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

    def getResponse(self, ingredients, numOfRecipes, rank, apiKey):
        url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={apiKey}&ingredients={ingredients}&number={numOfRecipes}&ranking={rank}"

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
    ingredientsList = []
    count = 0
    while True:
        ingredient = input("\nEnter the ingredient: ").lower().strip()
        if count == 0:
            ingredientsList.append(f"{ingredient}")
        else:
            ingredientsList.append(f"+{ingredient}")

        while True:
            try:
                response = input("\nDo you wish to add another ingredient? (y/n): ").lower()
                if response in ['y', 'n']:
                    break
            except:
                print("\nPlease input either y or n: ")

        if response == 'n':
            break

    numOfRecipesRequired = int(input("\nEnter the number of recipes you need (max: 100): "))

    rank = int(input("""
Press 1 to maximize available ingredients
Press 2 to minimize missing ingredients: """))

    ingredients = ",".join(ingredientsList)

    return ingredients, numOfRecipesRequired, rank


def main():
    recipes = Recipes()
    print("\nWelcome to Kartik's Recipe Finder!")

    apiKey = input("\nEnter the API Key: ")

    while True:
        count = 1
        ingredients, numOfRecipes, rank = getParameters()
        recipesFound = recipes.getResponse(ingredients, numOfRecipes, rank, apiKey)
        print("\nBelow are some recipes you could try: ")
        for item in recipesFound:
            print(f"{count}. {item}")
            count += 1

        again = input("\nDo you wish to search for recipes again?(y/n): ").lower()
        if again == 'n':
            break


if __name__ == '__main__':
    main()
import models
import claude

if __name__ == "__main__":
    conversation = "" 
    #TODO: get actual conversation format from discord to test UserPreferences model
    #TODO: parse last 10 messages from conversation and classify user intent e.g. looking for direct response // pointed questions
    #TODO: else: look for lulls in the conversation and get the thing going

    # users = ["Jay", "Oliver", "Emannuel"] #TODO: parse the users' unique key from the conversation & avoid IDs for now
    # preferences = {}
    # for user in users:
    #     preference_prompt = models.UserPreferences.build_prompt(user=user, conversation=conversation)
    #     response = claude.prompt(preference_prompt, model="claude-3-opus-20240229")
    #     preference = models.UserPreferences.model_validate_json(response)
    #     preferences[user] = preference

    # copy-pasta of test data
    preferences = [ { "user_id": "Jay", "dates": ["November", "December"], "budget": ["$1-2k"], "lodging": ["Airbnb"], "interests": ["golf", "good bars", "food"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Scottsdale, AZ"] }, { "user_id": "Oliver", "dates": ["November", "early December"], "budget": ["not over $2k"], "lodging": ["Airbnb"], "interests": ["active activities", "non-alcoholic venues"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Miami"] }, { "user_id": "Emannuel", "dates": ["November", "December"], "budget": ["around $1k"], "lodging": ["Airbnb"], "interests": ["comedy shows"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Denver"] } ]


    # perform research and format response
    # research_prompt = models.ResearchPath().build_prompt(type='research', preferences=preferences)
    # response = claude.prompt(research_prompt, model="claude-3-opus-20240229")
    # research = models.ResearchPath().model_validate_json(response)
    # response = claude.prompt(response_prompt, model="claude-3-opus-20240229")
    # print(response)

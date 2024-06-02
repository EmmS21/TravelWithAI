import models
import claude

if __name__ == "__main__":
    ## create new fact history first
    preferences = [ { "user_id": "Jay", "dates": ["November", "December"], "budget": ["$1-2k"], "lodging": ["Airbnb"], "interests": ["golf", "good bars", "food"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Scottsdale, AZ"] }, { "user_id": "Oliver", "dates": ["November", "early December"], "budget": ["not over $2k"], "lodging": ["Airbnb"], "interests": ["active activities", "non-alcoholic venues"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Miami"] }, { "user_id": "Emannuel", "dates": ["November", "December"], "budget": ["around $1k"], "lodging": ["Airbnb"], "interests": ["comedy shows"], "environment": ["warm climate"], "pace": ["flexible schedule"], "ambiguity": ["depends on the destination"], "risk": ["depends on the destination"], "travel_history": ["Denver"] } ]
    research_prompt = models.ResearchPath().build_prompt(type='research', preferences=preferences)
    response = claude.prompt(research_prompt, model="claude-3-opus-20240229")
    research = models.ResearchPath().model_validate_json(response)
    response_prompt = research.build_prompt(type='response', preferences=preferences)
    response = claude.prompt(response_prompt, model="claude-3-opus-20240229")
    print(response)
    print('success!')
    #TODO: get actual conversation going so we can do preferences + other one

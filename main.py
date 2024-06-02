import models
import claude
import json

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
    research_prompt = models.ResearchPath().build_research_prompt(preferences=preferences)
    # response = claude.prompt(research_prompt, model="claude-3-opus-20240229")
    response = {'questions': ['What specific dates in November or December work best for everyone?', 'Is everyone comfortable with a budget range of $1-2k per person?', 'Are there any other must-have activities or interests besides golf, bars, food, and comedy shows?', 'Does anyone have strong preferences on domestic vs international travel?', 'Are there any deal-breakers or things to avoid for the group (e.g. long flights, certain cuisines)?'], 'decision': ['The group has good alignment on travel dates (November/December), budget ($1-2k), lodging (Airbnb), and environment (warm climate).', 'Suggesting 2-3 specific warm weather destinations with a variety of activities would help narrow down the options.', "Providing more details on golf courses, bars, restaurants, and comedy venues in potential destinations would cater to the group's interests.", "Offering a mix of relaxing and active itinerary options would appeal to the group's desire for a flexible schedule.", 'Domestic destinations may be preferred to minimize travel time and avoid any international travel concerns.'], 'facts': ['Scottsdale, AZ has over 200 golf courses and is known for its vibrant nightlife and dining scene.', 'Miami offers world-famous beaches, a thriving comedy scene at venues like the Miami Improv, and top-rated restaurants.', 'San Diego boasts 70 miles of pristine beaches, over 90 golf courses, and a burgeoning craft beer and comedy club scene.', 'Austin, TX has a renowned food and bar scene, with over 1,000 food trucks and 250 live music venues.', 'New Orleans offers unique attractions like jazz clubs, comedy shows, ghost tours, and Creole and Cajun cuisine.']}
    research = models.ResearchPath.model_validate(response)
    response_prompt = research.build_response_prompt(preferences=preferences)
    print(response_prompt)
    # response = claude.prompt(response_prompt, model="claude-3-opus-20240229")
    # print(response)

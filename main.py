import models
import claude
import json

if __name__ == "__main__":
    conversation = """Alright, let's simulate a group chat between three friends (Alex, Sam, and Taylor) and a travel agent named Rachel. Here goes:
Alex: Hey everyone! I think it's about time we plan our annual friends' getaway. What do you all think?
Sam: I'm so in! It's been a crazy year, and I could definitely use a vacation.
Taylor: Count me in too! Where should we go this time?
Alex: I was thinking maybe a beach destination or a city with a lot of culture and history.
Sam: A beach sounds amazing! We could relax, soak up some sun, and try some water activities.
Taylor: I like the idea of exploring a new city too. We could visit museums, try local cuisine, and immerse ourselves in a different culture.
Alex: Why don't we loop in Rachel? She always has great suggestions. @Rachel, we need your expert advice!
Rachel: Hi everyone! It's great to hear from you. I'd be happy to help plan your annual getaway. Based on your interests, I have a few ideas in mind.
Sam: That's great, Rachel! What do you suggest?
Rachel: For a beach destination, I highly recommend Bali, Indonesia. It has stunning beaches, lush landscapes, and a vibrant culture. You can relax on the beach, visit ancient temples, and even try surfing!
Taylor: Bali sounds incredible! What about a city destination?
Rachel: If you're looking for a city rich in history and culture, I suggest Kyoto, Japan. It's known for its beautiful temples, gardens, and traditional architecture. You can also experience tea ceremonies, wear kimonos, and sample delicious Japanese cuisine.
Alex: Both options sound fantastic! What do you think, Sam and Taylor?
Sam: I'm leaning towards Bali for the beaches and relaxation, but Kyoto also sounds like an incredible cultural experience.
Taylor: I agree, both destinations are tempting! Rachel, could you give us a rough idea of the costs and best times to visit each place?
Here are a few key details about Bali and Kyoto to help with your decision:
Bali, Indonesia:

Best time to visit: May to September (dry season)
Average costs: $50-100 per person per day for accommodations, food, and activities
Highlights: Beautiful beaches, ancient temples, lush landscapes, surfing, vibrant culture

Kyoto, Japan:

Best time to visit: March to May (spring) or October to November (fall)
Average costs: $100-150 per person per day for accommodations, food, and activities
Highlights: Historic temples and shrines, traditional gardens, tea ceremonies, delicious cuisine, rich cultural heritage

Both destinations offer unique and memorable experiences. Bali may be better if your priority is relaxation and beach time, while Kyoto could be ideal if you're most interested in history, culture and city exploration.
Alex: Thanks for the breakdown, Rachel! Those details are super helpful.
Taylor: I'm torn - both places sound amazing for different reasons. The beaches of Bali are calling my name, but I'm also really intrigued by the cultural experiences in Kyoto.
Sam: I know what you mean, Taylor. It's a tough choice! I'm still leaning slightly towards Bali, but I could be persuaded either way.
Rachel: Based on everyone's interests in beaches, relaxation, and cultural experiences, I recommend Bali as the ideal destination for your group trip. Here's why:\n\n• Bali has world-class beaches like Nusa Dua, Seminyak, and Uluwatu for surfing, snorkeling, and beach clubs - perfect for Sam and Taylor who prioritize beach time and relaxation.\n\n• The Ubud area offers lush landscapes, rice terraces, traditional dance performances and art galleries for immersive cultural experiences that Alex and Taylor are seeking. \n\n• Accommodations range from luxury resorts to affordable villas and guesthouses, so there are options to fit different budgets.\n\nKyoto could also be a great choice for its rich history, 1,600+ temples, and renowned cuisine like kaiseki, tofu dishes and matcha. \n\nWhat does everyone think - are you leaning more towards the beaches of Bali or the cultural depth of Kyoto for this trip? Let me know and I can provide more tailored recommendations!
Alex: Wow, Rachel, you make excellent points about both destinations. I'm even more torn now! The cultural depth of Kyoto sounds incredible, but those Balinese beaches are so tempting.
Sam: I know, right? I was leaning towards Bali, but now I'm second-guessing myself. Kyoto's history and cuisine are really appealing too.
Taylor: Ugh, this is so hard! I love the idea of immersing ourselves in Kyoto's rich culture, but I also can't stop thinking about relaxing on a beautiful beach in Bali.
"""
    #TODO: get actual conversation format from discord to test UserPreferences model
    #TODO: create manual timer to track states and/or other business logic associated with all replies

    try:
        response = 'No calls to the API were made.'
        users = ["Taylor", "Alex", "Sam"] #TODO: parse the users' unique key from the conversation (currently hardcoded for testing purposes)
        
        research_prompt = models.ConversationState.build_research_prompt(users=users, conversation=conversation)
        response = claude.prompt(research_prompt)
        conversation_state = models.ConversationState.model_validate_json(response)
        ## go deeper into the conversation IFF we need to track preferences
        if conversation_state.state == 'question':
            preferences = {} # user:preference KVs
            for user in users:
                preference_prompt = models.UserPreferences.build_prompt(user=user, conversation=conversation)
                response = claude.prompt(preference_prompt)
                preference = models.UserPreferences.model_validate_json(response)
                preferences[user] = preference
            # perform research and format response
            research_prompt = models.ResearchPath().build_research_prompt(preferences=preferences)
            response = claude.prompt(research_prompt)
            research = models.ResearchPath.model_validate_json(response)
            response_prompt = research.build_response_prompt(preferences=preferences)
            response = claude.prompt(response_prompt)
            print(response)
        else:
            print(conversation_state.state)
            response_prompt = conversation_state.build_response_prompt(users=users, conversation=conversation)
            response = claude.prompt(response_prompt)
            print(response)
        print('success!')
    except Exception as e:
        print(response)
        print(e)
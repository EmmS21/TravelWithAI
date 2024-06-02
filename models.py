from pydantic import BaseModel, Field
from typing import ClassVar, Literal
import json

class PromptModel(BaseModel):
    role: str
    task: str
    flavor: str

def build_schema(schema) -> str:
    ## Generate JSON from the schema of BaseModel
    schema['properties'].pop('prompt', None)
    for key in schema['properties'].keys():
        schema['properties'][key].pop('title', None)
    return json.dumps(schema['properties'], indent=4)

## Reads the chat history and populates preferences
class UserPreferences(BaseModel):
    user_id: str = Field(description="Unique identifier provided above in the <user> XML tag.")
    dates: list[str] = Field(description="Date preferences user has in the form of either times preferred, times unavailable, or trip length.")
    budget: list[str] = Field(description="Budget preferences user has for the entire trip in the form of either budget ranges or sentiments.")
    lodging: list[str] = Field(description="Lodging preferences user has or specific accommodations e.g. lodging type, rooming situation, etc.")
    interests: list[str] = Field(description="Interests or preferred activities of the user e.g. native culture, museum visits, hiking, etc.")
    environment: list[str] = Field(description="Climate preferences of the user e.g. cityscape, summer vibes, domestic vs. international, nature/outdoors, etc.")
    pace: list[str] = Field(description="Pace the user likes to move e.g. packed itinerary, lazy mornings, etc.")
    ambiguity: list[str] = Field(description="The level of ambiguity user is able to tolerate when planning.")
    risk: list[str] = Field(description="The level of comfort user has with risky situations e.g. local crime rates, adventurous activities, etc.")
    avoid: list[str] = Field(description="Specific places or sorts of places the user has visited already and would prefer to avoid.")
    accept: list[str]  = Field(description="Specific places the user has expressed interest in and would prefer to visit or explore further.")

    prompt: ClassVar[PromptModel] = PromptModel(
        role="You are an experienced travel agent with deep customer empathy and a keen intuition for what people want despite whatever indecision holds them back. You are a part of a group chat where friends are discussing possible travel plans.",
        task="Your task is to parse the provided conversation in <conversation> XML tags above and fill in the data structure based on further instruction provided in <schema> XML tags with only escape-safe JSON. Focus on the specific user provided in <user> XML tags based on their responses in the conversation.",
        flavor="Skip the preamble. Avoid corporate jargon and gimmicks. Use concrete language that is grounded in something tangible. Be specific about the details but do not be arbitrary when deciding them. If there is no information supporting a user's preference, note that specific field as not enough information."
    )

    @classmethod
    def build_prompt(self, *, conversation: str = None, user: str = None) -> str:
        schema = build_schema(self.model_json_schema())
        prompt = f"""
            User: <user>{user}</user>
            Conversation: <conversation>{conversation}</conversation>
            \n{self.prompt.role}
            \n{self.prompt.task}
            Schema: <schema>{schema}</schema>
            \n{self.prompt.flavor}
            """
        return prompt

## Reads user preferences, generates questions to ask, and returns facts that reveal most information
class ResearchPath(BaseModel):
    questions: list[str] = Field(default_factory = list, description="Identify significant information gaps in the provided user preferences and generate questions that would move the conversation forward.")
    decision: list[str] = Field(default_factory = list, description="Identify how aligned the user preferences are, and whether alternative destinations or more in-depth suggestions would help move the conversation forward.")
    facts: list[str] = Field(default_factory = list, description="Identify facts about specific destinations or attractions that would help move the conversation forward.")
    # historical: list[str] = Field(default_factory = list, description="A list of historical facts already provided so we can avoid redundant conversation.")
                                  
    ## Identify the highest information gain
    research_prompt: ClassVar[PromptModel] = PromptModel(
        role="You are an experienced travel agent with deep customer empathy and a keen intuition for what people want despite whatever indecision holds them back. You are a part of a group chat where friends are discussing possible travel plans and your role is to move the conversation forward to break indecision.", ## You are expert travel agent 
        task="Your task is to list data, facts, destinations, and/or attractions based on the user preferences provided in <preferences> XML tags above and fill in the data structure based on further instruction provided in <schema> XML tags with only escape-safe JSON. Your thought process should be designed to tease out new preferences and opinions from the users and provide concrete data points to reference. When thinking, balance the preferences between each user, and drill-in where there is alignment between many users.",
        flavor="Skip the preamble. Avoid corporate jargon and gimmicks. Use concrete language that is grounded in something tangible. Be specific about the details but do not be arbitrary when deciding them. Use data-driven examples wherever possible. Be concise as possible and provide 5 bullet points for each list." ## 
    )

    ## Take new facts and transform this into a pretty response to send to the group
    response_prompt: ClassVar[PromptModel] = PromptModel(
        role="You are an experienced travel agent with deep customer empathy and a keen intuition for what people want despite whatever indecision holds them back. You are a part of a group chat where friends are discussing possible travel plans and your role is to move the conversation forward to break indecision.",
        task="Your task is to take the facts provided in <facts> XML tags and user preferences in <preferences> XML tags above and return a response designed to provide as much information as possible to the group. Your response should briefly summarize the user preferences in a single, concise sentence to set expectations for the new facts. Then provide the facts in the form of recommendations and suggestions.",
        flavor="Skip the preamble. Strive for simplicity and clarity. Use natural sounding and conversational language. Avoid slang, jargon, or other colloquialisms that make you sound like an aging baby boomer. Be concise, keep your messages short, and get to the point. Use data-driven examples wherever possible and bullets to organize information. Start your response with a a single specific and concrete recommendation based on user preferences, substantiate with more options & facts, and end the message by asking for a pulse check on the group's decision."
    )

    @classmethod
    def build_research_prompt(self, *, preferences: UserPreferences) -> str:
        schema = build_schema(self.model_json_schema())
        prompt = f"""
            Preferences: <preferences>{preferences}</preferences>
            \n{self.research_prompt.role}
            \n{self.research_prompt.task}
            Schema: <schema>{schema}</schema>
            \n{self.research_prompt.flavor}
            """
        return prompt

    def build_response_prompt(self, *, preferences:UserPreferences) -> str:
        prompt = f"""
            Preferences: <preferences>{preferences}</preferences>
            Facts: <facts>{self.facts}</facts>
            \n{self.response_prompt.role}
            \n{self.response_prompt.task}
            \n{self.response_prompt.flavor}
            """
        return prompt      
        
    ## TODO: leave to @Emmanuel for integration with Langchain
    def update_history(self, new_fact: list[str]) -> None:
        self.historical + new_fact

## reads the conversation, reads the user preferences, reads the fact history
class ConversationState(BaseModel):
    disengaged: list[str] = Field(description="Identify users who have not participated much at all in the conversation.")
    objectors: list[str] = Field(description="Identify users who have expressed strong opinions against certain destinations or activities.")
    attached: list[str] = Field(description="Identify users who have expressed strong opinions in favor of certain destinations or activities.")
    skeptics: list[str] = Field(description="Identify users who have expressed skepticism or doubt about the feasibility of certain destinations or activities.")

    prompt: ClassVar[PromptModel] = PromptModel(
        role="You are an experienced travel agent with deep customer empathy and a keen intuition for what people want despite whatever indecision holds them back. You are a part of a group chat where friends are discussing possible travel plans.",
        task="Your task is to parse the provided conversation in <conversation> XML tags above and fill in the data structure based on further instruction provided in <schema> XML tags with only escape-safe JSON. Where possible, orient your response to the most recent facts presented in <research> XML tags with the context provided in <preferences> XML tags.",
        flavor="Skip the preamble. Avoid corporate jargon and gimmicks. Use concrete language that is grounded in something tangible. Be specific about the details but do not be arbitrary when deciding them."
    )

    @classmethod
    def build_prompt(self, *, conversation: str, preferences: UserPreferences, research: ResearchPath) -> str:
        schema = build_schema(self.model_json_schema())
        prompt = f"""
            Conversation: <conversation>{conversation}</conversation>
            Preferences: <preferences>{preferences}</preferences>
            Research: <research>{research}</research>
            \n{self.prompt.role}
            \n{self.prompt.task}
            Schema: <schema>{schema}</schema>
            \n{self.prompt.flavor}
            """
        return prompt

from twilio.rest import Client
import os
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import dotenv
import discord
import models
import claude
import anthropic
import json
# from discord_slash import SlashCommand

dotenv.load_dotenv()
test = str(os.getenv("TOKEN"))
openAI = str(os.getenv("OPENAI"))

conversation = None
memory = None
intents = discord.Intents.all() 
intents.message_content = True
client = discord.Client(intents = intents)

guild_ids = [1246523804792914062]
users = ["Emmanuel"]
# def build_prompt():
    
@client.event
async def on_ready():
    print(f"{client.user} is ready and online!")

@client.event
async def on_guild_channel_create(channel):
    """This event is triggered when a channel is createed informing all users how the bot works"""
    welcome_message = """Hey everyone, thanks for inviting me to the group chat!
    My role here is to help y'all plan an amazing trip together by facilitating the conversation. You can think of think of this like any other group chat, except I'll be here answering research questions and driving the group toward an itinerary that works for everyone.
    To get us started -- does anyone have thoughts or suggestions for the group?"""
    await channel.send(welcome_message)


@client.event
async def on_member_join(member):
    await member.send(
        f'Welcome to the server, {member.mention}.'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    pre_order_convo = []
    async for message in message.channel.history():
        if not message.author.global_name: user_name = "bot"
        else: user_name = message.author.global_name
        pre_order_convo.append({user_name: message.content})
    conversation = pre_order_convo[::-1]
    print(conversation)
    try:
        response = 'No calls to the API were made.'
        users = ["Jay", "Oliver", "Emamanuel"] 
        research_prompt = models.ConversationState.build_research_prompt(users=users, conversation=conversation)
        response = claude.prompt(research_prompt)
        conversation_state = models.ConversationState.model_validate_json(response)
        if conversation_state.state == 'question':
            preferences = {} 
            for user in users:
                preference_prompt = models.UserPreferences.build_prompt(user=user, conversation=conversation)
                response = claude.prompt(preference_prompt)
                preference = models.UserPreferences.model_validate_json(response)
                preferences[user] = preference
            research_prompt = models.ResearchPath().build_research_prompt(preferences=preferences)
            response = claude.prompt(research_prompt)
            research = models.ResearchPath.model_validate_json(response)
            response_prompt = research.build_response_prompt(preferences=preferences)
            response = claude.prompt(response_prompt)
            print(response)
            await message.channel.send(response)
        else:
            print(conversation_state.state)
            response_prompt = conversation_state.build_response_prompt(users=users, conversation=conversation)
            response = claude.prompt(response_prompt)
            print(response)
            await message.channel.send(response)
    except Exception as e:
        print(response)
        print(e)

client.run(os.getenv('TOKEN'))
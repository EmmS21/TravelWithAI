from twilio.rest import Client
import os
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import dotenv
import discord

dotenv.load_dotenv()
bot = discord.Bot()
test = str(os.getenv("TOKEN"))
openAI = str(os.getenv("OPENAI"))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_member_join(member):
    await member.send(
        f'Welcome to the server, {member.mention}.'
    )

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

#testing whether bot returns total number of members in server
@bot.slash_command(name='count', description="Returns the total count of members")
async def count(ctx: discord.ApplicationContext):
    member_count = ctx.guild.member_count - 1 
    await ctx.respond(f'The number of members in this server is {member_count}.')

#needs to be aware of all the people in the group
#needs to ask each person questions to understand their preferences
#needs to structure the
@bot.slash_command(name='start', description="Starts the AI conversation")
async def preferences(ctx: discord.ApplicationContext):
    member_count = ctx.guild.member_count - 1
    template = """
    You are a travel agent, your task is to understand the preferences of all users in the group
    history: {history}
    Human: {input}
    """
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)
    context = {
            "input": f"Ask questions to all {member_count} members in the group.",
    }
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=openAI)
    memory = ConversationBufferMemory(memory_key="history")
    memory_variables = memory.load_memory_variables(inputs=context)
    context["history"] = memory_variables.get("history", "")
    conversation = ConversationChain(prompt=prompt_template, llm=llm, memory=memory)
    response = conversation.predict(input=context["input"], history=context["history"])
    memory.save_context(inputs={"input": context["input"]}, outputs={"history": response})
    await ctx.respond(response)
bot.run(os.getenv('TOKEN'))

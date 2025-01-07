import os
import discord
from discord.ext import commands
from discord import Intents
import random
import requests
import json
import pickle
from dotenv import load_dotenv
from discord.utils import get
import asyncio
from discord.ext import tasks
import time  # time for mining cooldowns
import tweepy
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TRON_API_KEY = os.getenv('TRON_API_KEY')

# Create Intents object
intents = Intents.default()
intents.members = True
intents.message_content = True

# Create bot with intents
bot = commands.Bot(command_prefix='!', intents=intents, help_command=commands.DefaultHelpCommand())

# Data storage
polls = {}
vortex_coins = {}
user_balances = {}
user_addresses = {}
coins = {}

# Sample question pool
questions_pool = {
    "programming": [
        {
            "question": "What is the difference between '==' and '===' in JavaScript?",
            "answer": "'==' compares values with type coercion, while '===' compares both values and types without coercion",
            "hint": "Think about type comparison"
        },
        {
            "question": "What is a closure in programming?",
            "answer": "A function that has access to variables in its outer scope even after the outer function has returned",
            "hint": "It's related to scope and variable access"
        },
        {
            "question": "What is the difference between let and var in JavaScript?",
            "answer": "let is block-scoped while var is function-scoped",
            "hint": "Think about variable scope"
        }
    ],
    "web_development": [
        {
            "question": "What does CSS stand for?",
            "answer": "Cascading Style Sheets",
            "hint": "It's related to styling web pages"
        },
        {
            "question": "What is the purpose of the DOCTYPE declaration?",
            "answer": "To tell the browser which version of HTML the page is written in",
            "hint": "It's the first line in an HTML document"
        },
        {
            "question": "What is REST in API development?",
            "answer": "Representational State Transfer, an architectural style for distributed systems",
            "hint": "It's a common approach for building web services"
        }
    ],
    "databases": [
        {
            "question": "What is the difference between SQL and NoSQL databases?",
            "answer": "SQL databases are relational and use structured tables, while NoSQL databases are non-relational and more flexible",
            "hint": "Think about data structure"
        },
        {
            "question": "What is an index in databases?",
            "answer": "A data structure that improves the speed of data retrieval operations",
            "hint": "It helps with query performance"
        }
    ],
    "cybersecurity": [
        {
            "question": "What is XSS in web security?",
            "answer": "Cross-Site Scripting, a type of injection attack where malicious scripts are inserted into trusted websites",
            "hint": "It's a common web vulnerability"
        },
        {
            "question": "What is a SQL injection attack?",
            "answer": "An attack that inserts malicious SQL code into database queries through user input",
            "hint": "It targets database operations"
        }
    ],
    "cloud_computing": [
        {
            "question": "What is the difference between IaaS, PaaS, and SaaS?",
            "answer": "They are different service models: Infrastructure as a Service, Platform as a Service, and Software as a Service",
            "hint": "Think about different levels of cloud service"
        },
        {
            "question": "What is containerization?",
            "answer": "A lightweight form of virtualization that packages applications with their dependencies",
            "hint": "Docker is a popular tool for this"
        }
    ],
    "artificial_intelligence": [
        {
            "question": "What is machine learning?",
            "answer": "A subset of AI that enables systems to learn and improve from experience without explicit programming",
            "hint": "It's about computers learning patterns"
        },
        {
            "question": "What is deep learning?",
            "answer": "A subset of machine learning using neural networks with multiple layers",
            "hint": "Think about neural networks"
        }
    ]
}

# Events
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Connected to {len(bot.guilds)} guilds')
    print(f'Bot latency: {round(bot.latency * 1000)}ms')
    auto_save.start()

# ... (include all the existing commands from dapp.py, cryptomining.py, quiz.py, and game.py)
# create a class or a way to get the commands working


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='greet')
    async def greet(self, ctx):
        await ctx.send('Hello!')



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if 'hello' in message.content.lower():
            await message.channel.send('Hi there!')

# To add the cog to the bot
bot.add_cog(MyCog(bot))

# Helper functions
def save_questions(questions, filename="questions.pkl"):
    with open(filename, 'wb') as file:
        pickle.dump(questions, file)

async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found.")

async def handle_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

def reward_coins(guild_id, user_id, coins_to_reward):
    if guild_id in vortex_coins:
        vortex_coins[guild_id][user_id] = vortex_coins[guild_id].get(user_id, 0) + coins_to_reward
    else:
        vortex_coins[guild_id] = {user_id: coins_to_reward}

class DappCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_poll(self, ctx, question: str, *options: str):
        if len(options) < 2:
            await ctx.send("A poll requires at least two options.")
            return
        if len(options) > 10:
            await ctx.send("A poll can have a maximum of 10 options.")
            return

        poll_id = len(polls) + 1
        polls[poll_id] = {'question': question, 'options': options, 'votes': {}}

        embed = discord.Embed(title="Poll",
                            description=question,
                            color=discord.Color.blue())
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i + 1}", value=option, inline=False)

        poll_message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_message.add_reaction(reactions[i])

    @commands.command()
    async def vote(self, ctx, poll_id: int, option_index: int):
        user = ctx.author
        if poll_id in polls:
            poll = polls[poll_id]
            if 0 <= option_index < len(poll['options']):
                poll['votes'][user.id] = option_index
                await ctx.send(f"{user.display_name} voted in poll {poll_id}.")
            else:
                await ctx.send("Invalid option index.")
        else:
            await ctx.send("Poll not found.")

    @commands.command()
    async def end_poll(self, ctx, poll_id: int):
        if poll_id in polls:
            poll = polls[poll_id]
            results = [0] * len(poll['options'])
            for vote in poll['votes'].values():
                results[vote] += 1
            result_message = "Poll Results:\n"
            for i, option in enumerate(poll['options']):
                result_message += f"Option {i + 1} ({option}): {results[i]} votes\n"
            await ctx.send(result_message)
            del polls[poll_id]
        else:
            await ctx.send("Poll not found.")

    @commands.command()
    @commands.has_role('Admin')
    async def add_premium(self, ctx, member: discord.Member):
        role = get(ctx.guild.roles, name="Premium")
        if not role:
            role = await ctx.guild.create_role(name="Premium", color=discord.Color.gold())
        await member.add_roles(role)
        await ctx.send(f"{member.display_name} has been given Premium membership.")

    @commands.command()
    @commands.has_role('Admin')
    async def remove_premium(self, ctx, member: discord.Member):
        role = get(ctx.guild.roles, name="Premium")
        if role:
            await member.remove_roles(role)
            await ctx.send(f"Premium membership removed from {member.display_name}.")
        else:
            await ctx.send("Premium role not found.")

    @commands.command()
    async def functionalities(self, ctx):
        print(f"Functionalities command triggered by {ctx.author}")  # Debug line
        functions = """
        **Available Commands:**
        
        **Quiz Commands:**
        • !quiz <category> - Start a quiz
        • !answer <your_answer> - Answer the current quiz
        • !hint - Get a hint for the current quiz
        
        **Economy Commands:**
        • !balance - Check your VortexCoin balance
        • !daily - Get daily reward
        • !transfer <@user> <amount> - Transfer VortexCoins
        • !leaderboard - View top 10 richest users
        
        **Mining Commands:**
        • !start_mining [rig_type] - Start mining (basic/medium/advanced)
        • !mining_stats - View mining rig statistics
        • !upgrade_rig - Check rig upgrade information
        
        **Poll Commands:**
        • !create_poll <question> <options> - Create a poll
        • !vote <poll_id> <option_index> - Vote in a poll
        • !end_poll <poll_id> - End a poll
        
        **Crypto Commands:**
        • !register_wallet <address> - Register your crypto wallet
        • !crypto_price <symbol> - Check crypto prices
        
        **Admin Commands:**
        • !add_premium <@user> - Grant premium membership
        • !remove_premium <@user> - Revoke premium membership
        """
        embed = discord.Embed(title="Bot Functionalities", description=functions, color=discord.Color.blue())
        await ctx.send(embed=embed)

# Add this before bot.run()
bot.add_cog(DappCog(bot))

class CryptoMining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mining_rates = {
            "basic": {"rate": 1, "cost": 0},
            "medium": {"rate": 2, "cost": 1000},
            "advanced": {"rate": 5, "cost": 5000}
        }
        self.active_miners = {}  # Store active mining sessions
        self.mining_cooldowns = {}  # Store mining cooldowns

    @commands.command(name='start_mining')
    async def start_mining(self, ctx, rig_type="basic"):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        # Check cooldown
        if user_id in self.mining_cooldowns:
            if time.time() - self.mining_cooldowns[user_id] < 3600:  # 1-hour cooldown
                remaining = 3600 - (time.time() - self.mining_cooldowns[user_id])
                await ctx.send(f"Mining cooldown active. Try again in {remaining:.0f} seconds.")
                return

        # Validate rig type
        if rig_type not in self.mining_rates:
            await ctx.send(f"Invalid rig type. Choose from: {', '.join(self.mining_rates.keys())}")
            return

        # Check if user can afford the rig
        user_balance = vortex_coins.get(guild_id, {}).get(user_id, 0)
        rig_cost = self.mining_rates[rig_type]["cost"]
        
        if user_balance < rig_cost:
            await ctx.send(f"You need {rig_cost} VortexCoins to use the {rig_type} mining rig!")
            return

        # Deduct rig cost if not basic
        if rig_cost > 0:
            vortex_coins[guild_id][user_id] -= rig_cost

        # Start mining session
        mining_rate = self.mining_rates[rig_type]["rate"]
        mining_duration = random.randint(30, 60)  # Random duration between 30-60 seconds
        reward = mining_rate * mining_duration

        await ctx.send(f"Started mining with {rig_type} rig! Mining for {mining_duration} seconds...")
        await asyncio.sleep(mining_duration)

        # Award coins
        reward_coins(guild_id, user_id, reward)
        self.mining_cooldowns[user_id] = time.time()
        
        await ctx.send(f"Mining complete! You earned {reward} VortexCoins!")

    @commands.command(name='mining_stats')
    async def mining_stats(self, ctx):
        embed = discord.Embed(title="Mining Statistics", color=discord.Color.gold())
        
        for rig, data in self.mining_rates.items():
            embed.add_field(
                name=f"{rig.capitalize()} Rig",
                value=f"Rate: {data['rate']} coins/sec\nCost: {data['cost']} VortexCoins",
                inline=False
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='upgrade_rig')
    async def upgrade_rig(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        user_balance = vortex_coins.get(guild_id, {}).get(user_id, 0)
        
        # Find current rig level
        current_rig = "basic"
        for rig in ["advanced", "medium", "basic"]:
            if user_balance >= self.mining_rates[rig]["cost"]:
                current_rig = rig
                break

        # Calculate next rig
        if current_rig == "basic":
            next_rig = "medium"
        elif current_rig == "medium":
            next_rig = "advanced"
        else:
            await ctx.send("You already have the best mining rig!")
            return

        upgrade_cost = self.mining_rates[next_rig]["cost"]
        await ctx.send(f"Your current rig: {current_rig}\nNext upgrade: {next_rig}\nCost: {upgrade_cost} VortexCoins")

    @commands.command(name='mining_help')
    async def mining_help(self, ctx):
        help_text = """
        **Mining Commands:**
        `!start_mining [rig_type]` - Start mining (basic/medium/advanced)
        `!mining_stats` - View mining rig statistics
        `!upgrade_rig` - Check rig upgrade information
        
        **Mining Rigs:**
        - Basic: Free, 1 coin/sec
        - Medium: 1000 VortexCoins, 2 coins/sec
        - Advanced: 5000 VortexCoins, 5 coins/sec
        
        Note: Mining has a 1-hour cooldown period.
        """
        await ctx.send(help_text)

# Add this before bot.run()
bot.add_cog(CryptoMining(bot))

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance')
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        balance = vortex_coins.get(guild_id, {}).get(user_id, 0)
        await ctx.send(f'Your balance: {balance} VortexCoins')

    @commands.command(name='daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        reward = 100
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        reward_coins(guild_id, user_id, reward)
        await ctx.send(f'You claimed your daily reward of {reward} VortexCoins!')

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_quizzes = {}
        self.scores = {}

    @commands.command(name='quiz')
    async def start_quiz(self, ctx, category=None):
        if category not in questions_pool:
            categories = ', '.join(questions_pool.keys())
            await ctx.send(f'Please specify a valid category: {categories}')
            return
        
        question_data = random.choice(questions_pool[category])
        await ctx.send(f"Question: {question_data['question']}\nUse !answer <your_answer> to respond")
        self.active_quizzes[ctx.channel.id] = {
            'data': question_data,
            'user': ctx.author.id,
            'attempts': 0
        }

    @commands.command(name='hint')
    async def hint(self, ctx):
        if ctx.channel.id in self.active_quizzes:
            quiz = self.active_quizzes[ctx.channel.id]
            if quiz['user'] == ctx.author.id:
                await ctx.send(f"Hint: {quiz['data']['hint']}")
            else:
                await ctx.send("This isn't your quiz!")
        else:
            await ctx.send("No active quiz in this channel!")

    @commands.command(name='answer')
    async def answer(self, ctx, *, answer: str):
        if ctx.channel.id in self.active_quizzes:
            quiz = self.active_quizzes[ctx.channel.id]
            
            if quiz['user'] != ctx.author.id:
                await ctx.send("This isn't your quiz!")
                return

            quiz['attempts'] += 1
            correct_answer = quiz['data']['answer'].lower()
            user_answer = answer.lower()

            if user_answer == correct_answer:
                # Calculate reward based on attempts
                reward = max(20 - (quiz['attempts'] - 1) * 5, 5)
                reward_coins(str(ctx.guild.id), str(ctx.author.id), reward)
                await ctx.send(f"Correct! You earned {reward} VortexCoins!")
                del self.active_quizzes[ctx.channel.id]
            else:
                if quiz['attempts'] >= 3:
                    await ctx.send(f"Sorry, you've run out of attempts. The correct answer was: {correct_answer}")
                    del self.active_quizzes[ctx.channel.id]
                else:
                    await ctx.send(f"Wrong answer! You have {3 - quiz['attempts']} attempts remaining. Try using !hint")

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register_wallet')
    async def register_wallet(self, ctx, wallet_address: str):
        user_id = str(ctx.author.id)
        user_addresses[user_id] = wallet_address
        await ctx.send(f'Wallet address registered successfully!')

    @commands.command(name='crypto_price')
    async def crypto_price(self, ctx, symbol: str):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()
            price = data[symbol.lower()]['usd']
            await ctx.send(f'{symbol.upper()} price: ${price:,.2f} USD')
        except:
            await ctx.send('Error fetching price. Make sure you used the correct coin ID.')

# Add this before bot.run()
bot.add_cog(Economy(bot))
bot.add_cog(Quiz(bot))
bot.add_cog(Crypto(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to use this command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument! Check !functionalities for command usage.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Invalid argument provided! Check !functionalities for command usage.')
    else:
        await handle_error(ctx, error)

# Save data periodically
def save_data():
    with open('vortex_data.pkl', 'wb') as f:
        pickle.dump({
            'vortex_coins': vortex_coins,
            'user_addresses': user_addresses,
            'polls': polls
        }, f)

# You might want to call save_data periodically using Discord's tasks instead
@tasks.loop(minutes=10)
async def auto_save():
    save_data()

# Start the auto-save when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Connected to {len(bot.guilds)} guilds')
    print(f'Bot latency: {round(bot.latency * 1000)}ms')
    auto_save.start()

async def setup():
    await bot.add_cog(DappCog(bot))
    await bot.add_cog(CryptoMining(bot))
    await bot.add_cog(Economy(bot))
    await bot.add_cog(Quiz(bot))
    await bot.add_cog(Crypto(bot))
    await bot.add_cog(NFTSystem(bot))
    await bot.add_cog(Governance(bot))
    await bot.add_cog(Marketplace(bot))

# Modify the bot.run line to this:
asyncio.run(setup())
bot.run(DISCORD_BOT_TOKEN)

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = {}
        
    @commands.command(name='level')
    async def check_level(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.levels:
            self.levels[user_id] = {"xp": 0, "level": 1}
        
        level_data = self.levels[user_id]
        embed = discord.Embed(title=f"{ctx.author.name}'s Level", color=discord.Color.blue())
        embed.add_field(name="Level", value=level_data["level"])
        embed.add_field(name="XP", value=f"{level_data['xp']}/100")
        await ctx.send(embed=embed)

    async def add_xp(self, user_id, xp_amount):
        if user_id not in self.levels:
            self.levels[user_id] = {"xp": 0, "level": 1}
            
        self.levels[user_id]["xp"] += xp_amount
        if self.levels[user_id]["xp"] >= 100:
            self.levels[user_id]["level"] += 1
            self.levels[user_id]["xp"] = 0
            return True
        return False

class EnhancedMining(CryptoMining):
    def __init__(self, bot):
        super().__init__(bot)
        self.mining_bonuses = {}
        self.staking_pools = {}

    @commands.command(name='mining_bonus')
    async def activate_bonus(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.mining_bonuses:
            self.mining_bonuses[user_id] = 1.5  # 50% bonus
            await ctx.send("🎉 Mining bonus activated! +50% rewards for 1 hour!")
            await asyncio.sleep(3600)  # 1 hour
            del self.mining_bonuses[user_id]
        else:
            await ctx.send("You already have an active mining bonus!")

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip')
    async def coinflip(self, ctx, bet: int, choice: str):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        if bet <= 0:
            await ctx.send("Bet must be positive!")
            return
            
        if vortex_coins[guild_id][user_id] < bet:
            await ctx.send("Insufficient funds!")
            return
            
        result = random.choice(['heads', 'tails'])
        if choice.lower() == result:
            reward_coins(guild_id, user_id, bet * 2)
            await ctx.send(f"🎉 You won! The coin landed on {result}!")
        else:
            vortex_coins[guild_id][user_id] -= bet
            await ctx.send(f"Sorry, you lost! The coin landed on {result}.")

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = {
            "mining_boost": {"price": 500, "description": "2x mining rewards for 1 hour"},
            "premium_badge": {"price": 5000, "description": "Exclusive premium badge"},
            "lottery_ticket": {"price": 100, "description": "Chance to win big!"}
        }

    @commands.command(name='shop')
    async def show_shop(self, ctx):
        embed = discord.Embed(title="VortexCoin Shop", color=discord.Color.green())
        for item, data in self.items.items():
            embed.add_field(
                name=f"{item.replace('_', ' ').title()} - {data['price']} coins",
                value=data['description'],
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def buy_item(self, ctx, item: str):
        if item not in self.items:
            await ctx.send("Invalid item!")
            return
            
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        price = self.items[item]["price"]
        
        if vortex_coins[guild_id][user_id] < price:
            await ctx.send("Insufficient funds!")
            return
            
        vortex_coins[guild_id][user_id] -= price
        await ctx.send(f"Successfully purchased {item}!")

class Challenges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_challenges = {}
        self.generate_challenges.start()

    @tasks.loop(hours=24)
    async def generate_challenges(self):
        self.daily_challenges = {
            "mine_coins": {"goal": 1000, "reward": 500, "description": "Mine 1000 vortexcoins"},
            "win_games": {"goal": 5, "reward": 300, "description": "Win 5 games"},
            "answer_quiz": {"goal": 3, "reward": 200, "description": "Answer 3 quiz questions"}
        }

    @commands.command(name='challenges')
    async def show_challenges(self, ctx):
        embed = discord.Embed(title="Daily Challenges", color=discord.Color.purple())
        for challenge, data in self.daily_challenges.items():
            embed.add_field(
                name=challenge.replace('_', ' ').title(),
                value=f"{data['description']} - Reward: {data['reward']} vortexcoins",
                inline=False
            )
        await ctx.send(embed=embed)

bot.add_cog(LevelSystem(bot))
bot.add_cog(EnhancedMining(bot))
bot.add_cog(Games(bot))
bot.add_cog(Shop(bot))
bot.add_cog(Challenges(bot))

class TwitterRaiding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_raids = {}
        self.raid_cooldowns = {}
        self.raid_participants = {}
        
        # Twitter API credentials (Add these to your .env file)
        auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
        auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        self.twitter_api = tweepy.API(auth)

    @commands.command(name='start_raid')
    @commands.has_role('Raid Manager')
    async def start_raid(self, ctx, tweet_url: str, duration: int = 30, reward: int = 100):
        """
        Start a new Twitter raid
        Usage: !start_raid <tweet_url> [duration_in_minutes] [reward_per_action]
        """
        try:
            # Extract tweet ID from URL
            tweet_id = tweet_url.split('/')[-1]
            tweet = self.twitter_api.get_status(tweet_id)
            
            raid_id = str(ctx.message.id)
            self.active_raids[raid_id] = {
                'tweet_id': tweet_id,
                'tweet_url': tweet_url,
                'start_time': datetime.now(),
                'duration': duration,
                'reward': reward,
                'participants': set(),
                'initial_metrics': {
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': 0  # Base count for replies
                }
            }

            raid_embed = discord.Embed(
                title="🚀 Twitter Raid Started!",
                description=f"Let's raid this tweet!\n{tweet_url}",
                color=discord.Color.blue()
            )
            raid_embed.add_field(name="Duration", value=f"{duration} minutes")
            raid_embed.add_field(name="Reward per Action", value=f"{reward} VortexCoins")
            raid_embed.add_field(name="Actions Required", 
                               value="✅ Like\n🔄 Retweet\n💭 Reply with meaningful content",
                               inline=False)

            await ctx.send(embed=raid_embed)
            
            # Schedule raid end
            self.bot.loop.create_task(self.end_raid(ctx, raid_id))

        except tweepy.TweepError as e:
            await ctx.send(f"Error accessing tweet: {str(e)}")

    @commands.command(name='join_raid')
    async def join_raid(self, ctx, raid_id: str, twitter_username: str):
        """
        Join an active raid
        Usage: !join_raid <raid_id> <your_twitter_username>
        """
        if raid_id not in self.active_raids:
            await ctx.send("Invalid raid ID or raid has ended!")
            return

        raid = self.active_raids[raid_id]
        user_id = str(ctx.author.id)

        # Check if user is on cooldown
        if user_id in self.raid_cooldowns:
            if datetime.now() < self.raid_cooldowns[user_id]:
                remaining = (self.raid_cooldowns[user_id] - datetime.now()).seconds
                await ctx.send(f"You're on raid cooldown! Try again in {remaining} seconds.")
                return

        # Add user to raid participants
        raid['participants'].add(user_id)
        self.raid_participants[user_id] = twitter_username

        await ctx.send(f"You've joined the raid! Complete the required actions on Twitter using account @{twitter_username}")

    @commands.command(name='verify_raid')
    async def verify_raid(self, ctx, raid_id: str):
        """
        Verify user's raid participation
        Usage: !verify_raid <raid_id>
        """
        if raid_id not in self.active_raids:
            await ctx.send("Invalid raid ID or raid has ended!")
            return

        raid = self.active_raids[raid_id]
        user_id = str(ctx.author.id)

        if user_id not in raid['participants']:
            await ctx.send("You haven't joined this raid!")
            return

        try:
            twitter_username = self.raid_participants[user_id]
            tweet = self.twitter_api.get_status(raid['tweet_id'])
            
            # Verify user's actions
            actions_completed = 0
            reward_earned = 0

            # Check like
            if self.verify_like(tweet.id, twitter_username):
                actions_completed += 1
                reward_earned += raid['reward']

            # Check retweet
            if self.verify_retweet(tweet.id, twitter_username):
                actions_completed += 1
                reward_earned += raid['reward']

            # Check reply
            if self.verify_reply(tweet.id, twitter_username):
                actions_completed += 1
                reward_earned += raid['reward']

            # Award VortexCoins
            if actions_completed > 0:
                guild_id = str(ctx.guild.id)
                reward_coins(guild_id, user_id, reward_earned)
                
                # Set cooldown
                self.raid_cooldowns[user_id] = datetime.now() + timedelta(hours=1)

                await ctx.send(f"Raid participation verified! You completed {actions_completed} actions and earned {reward_earned} VortexCoins!")
            else:
                await ctx.send("No raid actions verified. Make sure to like, retweet, and reply to the tweet!")

        except tweepy.TweepError as e:
            await ctx.send(f"Error verifying raid actions: {str(e)}")

    async def end_raid(self, ctx, raid_id: str):
        """
        End the raid after duration expires
        """
        raid = self.active_raids[raid_id]
        await asyncio.sleep(raid['duration'] * 60)  # Convert minutes to seconds

        try:
            tweet = self.twitter_api.get_status(raid['tweet_id'])
            
            # Calculate raid impact
            final_metrics = {
                'likes': tweet.favorite_count - raid['initial_metrics']['likes'],
                'retweets': tweet.retweet_count - raid['initial_metrics']['retweets'],
                'participants': len(raid['participants'])
            }

            # Create raid summary embed
            summary_embed = discord.Embed(
                title="📊 Raid Summary",
                description=f"Raid on {raid['tweet_url']} has ended!",
                color=discord.Color.green()
            )
            summary_embed.add_field(name="New Likes", value=final_metrics['likes'])
            summary_embed.add_field(name="New Retweets", value=final_metrics['retweets'])
            summary_embed.add_field(name="Participants", value=final_metrics['participants'])

            await ctx.send(embed=summary_embed)
            del self.active_raids[raid_id]

        except tweepy.TweepError as e:
            await ctx.send(f"Error generating raid summary: {str(e)}")

    def verify_like(self, tweet_id, username):
        """Verify if user liked the tweet"""
        try:
            likes = self.twitter_api.get_favorites(tweet_id)
            return any(like.user.screen_name.lower() == username.lower() for like in likes)
        except:
            return False

    def verify_retweet(self, tweet_id, username):
        """Verify if user retweeted the tweet"""
        try:
            retweets = self.twitter_api.get_retweets(tweet_id)
            return any(rt.user.screen_name.lower() == username.lower() for rt in retweets)
        except:
            return False

    def verify_reply(self, tweet_id, username):
        """Verify if user replied to the tweet"""
        try:
            replies = self.twitter_api.search(q=f"to:{username}", since_id=tweet_id)
            return any(reply.in_reply_to_status_id == tweet_id for reply in replies)
        except:
            return False

    @commands.command(name='raid_help')
    async def raid_help(self, ctx):
        """Display help information about raids"""
        help_embed = discord.Embed(
            title="Twitter Raid Help",
            description="Help guide for Twitter raid commands",
            color=discord.Color.blue()
        )
        help_embed.add_field(
            name="Start a Raid",
            value="!start_raid <tweet_url> [duration_in_minutes] [reward_per_action]",
            inline=False
        )
        help_embed.add_field(
            name="Join a Raid",
            value="!join_raid <raid_id> <your_twitter_username>",
            inline=False
        )
        help_embed.add_field(
            name="Verify Participation",
            value="!verify_raid <raid_id>",
            inline=False
        )
        await ctx.send(embed=help_embed)

# Add to bot setup
bot.add_cog(TwitterRaiding(bot))

class NFTSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nft_collection = {}
        self.marketplace = {}

    @commands.command(name='mint_nft')
    async def mint_nft(self, ctx, name: str, description: str):
        user_id = str(ctx.author.id)
        nft_id = len(self.nft_collection) + 1
        
        # Create NFT
        nft = {
            'id': nft_id,
            'name': name,
            'description': description,
            'owner': user_id,
            'created_at': datetime.now(),
            'rarity': random.choice(['common', 'rare', 'epic', 'legendary'])
        }
        
        self.nft_collection[nft_id] = nft
        await ctx.send(f"NFT #{nft_id} minted successfully!")

    @commands.command(name='list_nft')
    async def list_nft(self, ctx, nft_id: int, price: int):
        user_id = str(ctx.author.id)
        if nft_id in self.nft_collection and self.nft_collection[nft_id]['owner'] == user_id:
            self.marketplace[nft_id] = price
            await ctx.send(f"NFT #{nft_id} listed for {price} VortexCoins")

class Governance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.proposals = {}
        self.votes = {}

    @commands.command(name='create_proposal')
    @commands.has_role('Governance')
    async def create_proposal(self, ctx, title: str, *, description: str):
        proposal_id = len(self.proposals) + 1
        self.proposals[proposal_id] = {
            'title': title,
            'description': description,
            'creator': ctx.author.id,
            'votes_for': 0,
            'votes_against': 0,
            'active': True,
            'created_at': datetime.now()
        }
        
        embed = discord.Embed(
            title=f"Proposal #{proposal_id}: {title}",
            description=description,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

class Marketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listings = {}
        self.orders = {}

    @commands.command(name='create_listing')
    async def create_listing(self, ctx, item_name: str, price: int, quantity: int = 1):
        listing_id = len(self.listings) + 1
        self.listings[listing_id] = {
            'seller': ctx.author.id,
            'item': item_name,
            'price': price,
            'quantity': quantity,
            'active': True
        }
        
        embed = discord.Embed(
            title="New Marketplace Listing",
            description=f"{item_name} x{quantity}",
            color=discord.Color.green()
        )
        embed.add_field(name="Price", value=f"{price} VortexCoins")
        await ctx.send(embed=embed)

class EquitySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shares = {}  # Format: {guild_id: {user_id: shares_amount}}
        self.total_shares = {}  # Format: {guild_id: total_shares}
        self.share_history = {}  # Format: {guild_id: [{timestamp, from_user, to_user, amount}]}

    @commands.command(name='grant_shares')
    @commands.has_role('Owner')  # Only server owner can grant initial shares
    async def grant_shares(self, ctx, member: discord.Member, amount: int):
        """Grant shares to a team member"""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        # Initialize dictionaries if needed
        if guild_id not in self.shares:
            self.shares[guild_id] = {}
            self.total_shares[guild_id] = 0
            self.share_history[guild_id] = []

        # Update shares
        self.shares[guild_id][user_id] = self.shares[guild_id].get(user_id, 0) + amount
        self.total_shares[guild_id] += amount

        # Record transaction
        self.share_history[guild_id].append({
            'timestamp': datetime.now(),
            'from_user': str(ctx.author.id),
            'to_user': user_id,
            'amount': amount
        })

        # Create embed message
        embed = discord.Embed(
            title="🎉 Shares Granted",
            description=f"{member.mention} has been granted {amount} shares",
            color=discord.Color.green()
        )
        embed.add_field(name="Total Shares", value=f"{self.shares[guild_id][user_id]:,}")
        embed.add_field(name="Ownership %", 
                       value=f"{(self.shares[guild_id][user_id] / self.total_shares[guild_id] * 100):.2f}%")

        await ctx.send(embed=embed)

    @commands.command(name='shares')
    async def check_shares(self, ctx, member: discord.Member = None):
        """Check shares for yourself or another member"""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id if member else ctx.author.id)
        
        if guild_id not in self.shares or user_id not in self.shares[guild_id]:
            await ctx.send("No shares found.")
            return

        shares_amount = self.shares[guild_id][user_id]
        ownership_percent = (shares_amount / self.total_shares[guild_id] * 100)

        embed = discord.Embed(
            title="📊 Share Information",
            color=discord.Color.blue()
        )
        embed.add_field(name="Shares Owned", value=f"{shares_amount:,}")
        embed.add_field(name="Ownership %", value=f"{ownership_percent:.2f}%")
        embed.add_field(name="Total Project Shares", value=f"{self.total_shares[guild_id]:,}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='transfer_shares')
    async def transfer_shares(self, ctx, recipient: discord.Member, amount: int):
        """Transfer shares to another team member"""
        guild_id = str(ctx.guild.id)
        sender_id = str(ctx.author.id)
        recipient_id = str(recipient.id)

        # Check if sender has enough shares
        if (guild_id not in self.shares or 
            sender_id not in self.shares[guild_id] or 
            self.shares[guild_id][sender_id] < amount):
            await ctx.send("Insufficient shares for transfer.")
            return

        # Perform transfer
        self.shares[guild_id][sender_id] -= amount
        self.shares[guild_id][recipient_id] = self.shares[guild_id].get(recipient_id, 0) + amount

        # Record transaction
        self.share_history[guild_id].append({
            'timestamp': datetime.now(),
            'from_user': sender_id,
            'to_user': recipient_id,
            'amount': amount
        })

        embed = discord.Embed(
            title="🔄 Shares Transferred",
            description=f"{amount:,} shares transferred to {recipient.mention}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='share_history')
    async def view_history(self, ctx, limit: int = 5):
        """View recent share transactions"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.share_history or not self.share_history[guild_id]:
            await ctx.send("No share history found.")
            return

        embed = discord.Embed(
            title="📜 Share Transaction History",
            color=discord.Color.gold()
        )

        for transaction in reversed(self.share_history[guild_id][-limit:]):
            from_user = await self.bot.fetch_user(int(transaction['from_user']))
            to_user = await self.bot.fetch_user(int(transaction['to_user']))
            
            embed.add_field(
                name=f"Transfer on {transaction['timestamp'].strftime('%Y-%m-%d %H:%M')}",
                value=f"From: {from_user.name}\nTo: {to_user.name}\nAmount: {transaction['amount']:,} shares",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name='share_distribution')
    async def view_distribution(self, ctx):
        """View current share distribution"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.shares:
            await ctx.send("No shares have been distributed yet.")
            return

        embed = discord.Embed(
            title="📊 Share Distribution",
            description=f"Total Shares: {self.total_shares[guild_id]:,}",
            color=discord.Color.purple()
        )

        # Sort holders by share amount
        holders = sorted(
            self.shares[guild_id].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for user_id, shares in holders:
            user = await self.bot.fetch_user(int(user_id))
            percentage = (shares / self.total_shares[guild_id] * 100)
            embed.add_field(
                name=user.name,
                value=f"Shares: {shares:,} ({percentage:.2f}%)",
                inline=False
            )

        await ctx.send(embed=embed)

# Add to your bot setup
bot.add_cog(EquitySystem(bot))
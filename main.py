import os
import discord
from discord.ext import commands
from routes.utils import app, token
from quart import Quart, redirect, url_for, render_template, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

client = commands.Bot(command_prefix='//', intents=discord.Intents.default())

app = Quart(__name__)

app.secret_key = os.environ.get("session")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = os.environ.get("client_id")
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get("client_secret")
app.config["DISCORD_REDIRECT_URI"] = os.environ.get("ri")
app.config["DISCORD_BOT_TOKEN"] = os.environ.get("token")
discordd = DiscordOAuth2Session(app)


@app.route("/")
async def home():
    logged = ""
    if await discordd.authorized:
        logged = True
    return await render_template("index.html", logged=logged)


@app.route("/login/")
async def login():
    return await discordd.create_session(scope=["identify", "guilds"])


@app.route("/logout/")
async def logout():
    discordd.revoke()
    return redirect(url_for(".home"))


@app.route("/me/")
@requires_authorization
async def me():
    user = await discordd.fetch_user()
    return redirect(url_for(".home"))


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    bot.url = request.url
    return redirect(url_for(".login"))


@app.route("/callback/")
async def callback():
    await discordd.callback()
    try:
        return redirect(bot.url)
    except:
        return redirect(url_for(".me"))


def run():
    client.loop.create_task(app.run_task('0.0.0.0'))


if __name__ == '__main__':
    run()

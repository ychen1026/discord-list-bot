from dotenv import load_dotenv
from interactions import (
        Client, Intents, listen,
        slash_command, slash_option, OptionType, SlashContext
        )
import os
import list_db as ldb

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = Client(intents=Intents.DEFAULT |
                     Intents.GUILD_PRESENCES |
                     Intents.GUILD_MEMBERS)

@listen()
async def on_ready():
    print("ready")
    print("following are the available application commands")
    for cmd in bot.application_commands:
        print(cmd.resolved_name)
    

@slash_command(name="slander", description="slander yoof")
async def slash_slander(ctx: SlashContext):
    await ctx.send("yoof sucks at valo")

@slash_command(name="list")
async def slash_list(ctx: SlashContext):
    pass

@slash_list.subcommand(sub_cmd_name="new", sub_cmd_description="creates a new list")
@slash_option(
        name="list-name",
        argument_name="list_name",
        description="the name of the list to create",
        required=True,
        opt_type=OptionType.STRING
        )
async def slash_list_new(ctx: SlashContext, list_name: str):
    list_name = list_name.lower() # clean the list name

    if await ldb.insert_new_list(int(ctx.guild_id), list_name) == -1:
        await ctx.send(f"{list_name} already exists!\n")
        return
    await ctx.send(f"created a new list called {list_name}!\n")

@slash_list.subcommand(sub_cmd_name="show", sub_cmd_description="show current lists or contents of the list if a list name is provided")
@slash_option(
        name="list-name",
        argument_name="list_name",
        description="show all lists or the contents of a given list",
        required=False,
        opt_type=OptionType.STRING
        )
async def slash_list_show(ctx: SlashContext, list_name: str=""):
    list_name = list_name.lower()

    print(list_name, len(list_name))
    if len(list_name) > 0:
        res = await ldb.show_items_in_list(int(ctx.guild_id), list_name)
    else:       
        res = await ldb.show_all_lists(int(ctx.guild_id))
    if res == []:
        await ctx.send("Either list is empty or does not exists!\n")
        return
    await ctx.send("\n".join(res))

@slash_list.subcommand(sub_cmd_name="add", sub_cmd_description="adds an item to a list")
@slash_option(
        name="list-name",
        argument_name="list_name",
        description="the name of the list to add the item to",
        required=True,
        opt_type=OptionType.STRING
        )
@slash_option(
        name="item-name",
        argument_name="item",
        description="the name of the item that will be added to the list",
        required=True,
        opt_type=OptionType.STRING
        )
async def slash_list_add(ctx: SlashContext, list_name: str, item: str):
    list_name = list_name.lower() # clean the list name

    if await ldb.insert_item_to_list(int(ctx.guild_id), list_name, item) == -1:
        await ctx.send("Either item exists or list is not created!\n")
        return
    await ctx.send(f'{item} added to the {list_name} list!\n')


@slash_list.subcommand(sub_cmd_name="remove-list", sub_cmd_description="removes a list")
@slash_option(
        name="list-name",
        argument_name="list_name",
        description="the name of the list to remove",
        required=True,
        opt_type=OptionType.STRING
        )
async def slash_list_remove_list(ctx: SlashContext, list_name: str):
    await ldb.delete_list(int(ctx.guild_id), list_name)
    await ctx.send("list deleted!\n")
    
@slash_list.subcommand(sub_cmd_name="delete-item", sub_cmd_description="deletes a item from list")
@slash_option(
        name="list-name",
        argument_name="list_name",
        description="the name of the list to del the item from",
        required=True,
        opt_type=OptionType.STRING
        )
@slash_option(
        name="item-name",
        argument_name="item_name",
        description="the name of the item to del",
        required=True,
        opt_type=OptionType.STRING
        )
async def slash_list_delete_item(ctx: SlashContext, list_name: str, item_name):
    await ldb.delete_item(int(ctx.guild_id), list_name, item_name)
    await ctx.send("list deleted!\n")

bot.start(bot_token)

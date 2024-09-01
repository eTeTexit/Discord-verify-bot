import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


TARGET_GUILD_ID = 12345678910111213


verification_roles = {}
verification_channels = {}

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.id != TARGET_GUILD_ID:
            await interaction.response.send_message("This command is not available in this server.", ephemeral=True)
            return

        role_id = verification_roles.get(interaction.guild.id)
        if role_id:
            role = interaction.guild.get_role(role_id)
            if role:
                try:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"{interaction.user.mention}, you have been verified!", ephemeral=True)
                except discord.errors.Forbidden:
                    await interaction.response.send_message("I do not have permission to add roles. Please contact an admin.", ephemeral=True)
            else:
                await interaction.response.send_message("Verification role not found. Please contact an admin.", ephemeral=True)
        else:
            await interaction.response.send_message("Verification role not set. Please contact an admin.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        guild = discord.Object(id=TARGET_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f'Successfully synced commands for guild {TARGET_GUILD_ID}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="add_verify_button", description="Add a verify button to a channel")
async def add_verify_button(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.guild.id != TARGET_GUILD_ID:
        await interaction.response.send_message("This command is not available in this server.", ephemeral=True)
        return

    view = VerifyButton()
    await channel.send("Click the button below to verify yourself:", view=view)
    await interaction.response.send_message(f"Verify button added to {channel.mention}", ephemeral=True)

@bot.tree.command(name="set_verify_role", description="Set the verification role for the server")
async def set_verify_role(interaction: discord.Interaction, role: discord.Role):
    if interaction.guild.id != TARGET_GUILD_ID:
        await interaction.response.send_message("This command is not available in this server.", ephemeral=True)
        return

    verification_roles[interaction.guild.id] = role.id
    await interaction.response.send_message(f"Verification role set to {role.name}", ephemeral=True)

@bot.tree.command(name="help", description="Show available commands")
async def help_command(interaction: discord.Interaction):
    if interaction.guild.id != TARGET_GUILD_ID:
        await interaction.response.send_message("This command is not available in this server.", ephemeral=True)
        return

    help_text = (
        "/add_verify_button <channel>: Add a verify button to a specified channel.\n"
        "/set_verify_role <role>: Set the verification role for the server.\n"
        "/help: Show this help message.\n"
        "/support: Show support information."
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.tree.command(name="support", description="Show support information")
async def support_command(interaction: discord.Interaction):
    if interaction.guild.id != TARGET_GUILD_ID:
        await interaction.response.send_message("This command is not available in this server.", ephemeral=True)
        return

    support_text = (
        "For support, please contact the server admins or visit our support website at https://support.example.com"
    )
    await interaction.response.send_message(support_text, ephemeral=True)

    bot.run('')
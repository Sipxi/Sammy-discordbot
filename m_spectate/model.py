import discord.utils

class Spectators:


    def get_categories(self, guild):
        categories = []
        for category in guild.categories:
            if category is not None:
                categories.append(category)
        return categories

        
    def get_admin_roles(self, member_list):
        admin_roles = []
        for member in member_list:
            if member.guild_permissions.kick_members:
                admin_roles.append(member.roles[-1])
        return admin_roles
    
    def get_expected(self, guild):
        expected_role = discord.utils.get(guild.roles, name = "Spectator")
        expected_category = discord.utils.get(guild.categories, name="spectators")
        expected_channel = discord.utils.get(guild.channels, name="game-channel")
        expected_voice_channel = discord.utils.get(guild.channels, name="Voice game channel")
        return expected_role, expected_channel, expected_category, expected_voice_channel



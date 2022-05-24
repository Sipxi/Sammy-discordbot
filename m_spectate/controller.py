import discord
from .model import Spectators
class SpectatorsController:
    def __init__(self):
        self.model = Spectators()
        self.admin_roles = None
    


    async def run(self,guild):
        member_list = guild.members
        self.admin_roles = self.model.get_admin_roles(member_list)
        expected_role, expected_category = await self.create_expected_channels(guild)
        categories = self.model.get_categories(guild)
        await self.add_spectator_role(member_list, expected_role)
        await self.add_admin_permissions(expected_category)
        await self.block_permissions(categories, expected_role, expected_category)
    

    async def add_spectator_role(self, member_list, expected_role):
        for member in member_list:
            flag = False
            check = any(elem in self.admin_roles for elem in member.roles)
            for role in member.roles:
                if role == expected_role:
                    flag = True
            if not check and flag == False:
                await self.delete_not_needed_roles(member)
                await member.add_roles(expected_role)

    async def create_expected_channels(self,guild):
        expected_role, expected_channel, expected_category, expected_voice_channel= self.model.get_expected(guild)

        if expected_role is None:
            expected_role = await guild.create_role(name = "Spectator", colour = discord.Colour.dark_gray())

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            expected_role: discord.PermissionOverwrite(view_channel = True),}

        if expected_category is None:
            expected_category = await guild.create_category(name = "spectators", overwrites = overwrites)
        if expected_channel is None:
            expected_channel = await guild.create_text_channel(name = "game-channel" , category=expected_category)
        if expected_voice_channel is None:
            expected_voice_channel = await guild.create_voice_channel(name = "Voice game channel", category=expected_category)

        await expected_category.set_permissions(expected_role,view_channel=True)
        return expected_role, expected_category

    async def add_admin_permissions(self,expected_category):
        for role in self.admin_roles:
            await expected_category.set_permissions(role,view_channel=True,
            manage_channels = True, move_members = True, manage_messages = True, 
            mute_members = True, deafen_members =True)
    
    async def block_permissions(self, categories, expected_role, expected_category):
        if expected_category in categories:
            categories.remove(expected_category)
        else:
            await self.create_expected_channels()
            
        for category in categories:
            await category.set_permissions(expected_role,view_channel=False)
    
    async def delete_not_needed_roles(self, member):
        for role in member.roles:
            try:
                await member.remove_roles(role)
            except:
                pass







    





from orator.seeds import Seeder
from seeds.ChannelTableSeeder import ChannelTableSeeder
from seeds.SmsTableSeeder import SmsTableSeeder
from seeds.UserTableSeeder import UserTableSeeder

class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(ChannelTableSeeder)
        self.call(SmsTableSeeder)
        self.call(UserTableSeeder)




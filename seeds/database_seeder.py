from orator.seeds import Seeder
from seeds.ChannelTableSeeder import ChannelTableSeeder
from seeds.SmsTableSeeder import SmsTableSeeder

class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(ChannelTableSeeder)
        self.call(SmsTableSeeder)




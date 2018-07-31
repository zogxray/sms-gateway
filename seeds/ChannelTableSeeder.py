from orator.seeds import Seeder
from models.channel import Channel


class ChannelTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('channels').insert({
            'name': 'MTS for dummy',
            'phone': '+380956307619',
            'sim_id': 'thatispass',
            'sim_pass': 'thatispass',
            'balance': 100.30,
            'balance_ussd': '*101#'
        })


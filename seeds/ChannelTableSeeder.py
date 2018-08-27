from orator.seeds import Seeder
from models.channel import Channel


class ChannelTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('channels').insert({
            'name': 'For dummy',
            'phone': '+345645646456',
            'sim_id': '45634563456',
            'sim_pass': '435634564356',
            'balance': 100.30,
            'smpp_sim_id': 'id01',
            'smpp_sim_pass': 'pass',
            'smpp_sim_address': '192.168.1.2',
            'smpp_sim_port': 7777,
            'balance_ussd': '*101#'
        })

        self.db.table('channels').insert({
            'name': 'For raccoons',
            'phone': '+345645644566',
            'sim_id': '456345634566',
            'sim_pass': '435634564466',
            'balance': 100.30,
            'smpp_sim_id': 'id02',
            'smpp_sim_pass': 'pass',
            'smpp_sim_address': '192.168.1.2',
            'smpp_sim_port': 7777,
            'balance_ussd': '*101#'
        })


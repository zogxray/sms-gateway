from orator.seeds import Seeder
from orator.orm import Factory
from models.sms import Sms
from models.channel import Channel
import random

factory = Factory()

@factory.define(Sms)
def sms_factory(faker):
    return {
        'phone': faker.phone_number(),
        'text': faker.text(),
        'channel_id': Channel.first().id,
        'direction': False

    }

class SmsTableSeeder(Seeder):
    factory = factory
    def run(self):
        """
        Run the database seeds.
        """
        self.factory(Sms, 500).create()



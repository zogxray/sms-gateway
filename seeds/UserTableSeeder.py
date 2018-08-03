from orator.seeds import Seeder
from werkzeug.security import generate_password_hash

class UserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('users').insert({
            'login': 'zogxray@gmail.com',
            'password': generate_password_hash('777777'),
        })

        self.db.table('users').insert({
            'login': 'anna@gmail.com',
            'password': generate_password_hash('777777'),
        })

        self.db.table('users').insert({
            'login': 'senchuk@gmail.com',
            'password': generate_password_hash('777777'),
        })


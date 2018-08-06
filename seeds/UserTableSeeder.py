from orator.seeds import Seeder
from werkzeug.security import generate_password_hash

class UserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('users').insert({
            'login': 'zogxray@gmail.com',
            'password': generate_password_hash('6prxk6ap'),
        })

        self.db.table('users').insert({
            'login': 'a.flora@gepur.org',
            'password': generate_password_hash('ZnSBsNMr'),
        })

        self.db.table('users').insert({
            'login': 'admin@gepur.org',
            'password': generate_password_hash('UwuzTP8e'),
        })


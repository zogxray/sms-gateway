from orator.seeds import Seeder
from werkzeug.security import generate_password_hash

class UserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('users').insert({
            'login': 'test@test.com',
            'password': generate_password_hash('777777'),
        })


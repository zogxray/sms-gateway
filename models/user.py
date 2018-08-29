from orator import Model


class User(Model):
    __table__ = 'users'
    __fillable__ = ['login', 'password', 'expired_at']
    __dates__ = ['expired_at']
    __hidden__ = ['password']


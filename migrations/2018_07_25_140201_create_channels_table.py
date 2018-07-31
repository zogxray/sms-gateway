from orator.migrations import Migration


class CreateChannelsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('channels') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('sim_id').unique()
            table.string('sim_pass').unique()
            table.string('phone').unique()
            table.decimal('balance', 5, 2).default(0.00)
            table.timestamp('last_live_at').nullable()
            table.string('address').nullable()
            table.integer('port').nullable()
            table.string('balance_ussd').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('channels')

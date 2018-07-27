from orator.migrations import Migration


class CreateUssdTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('ussd') as table:
            table.big_increments('id')
            table.string('ussd')
            table.text('answer').nullable()
            table.timestamp('send_at').nullable()
            table.timestamp('received_at').nullable()

            table.integer('channel_id').unsigned()
            table.foreign('channel_id').references('id').on('channels').on_delete('cascade')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('ussd')

from orator.migrations import Migration


class CreateSmsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('sms') as table:
            table.increments('id')

            table.string('phone')
            table.string('text')
            table.integer('sim_msg_count').default(0)
            table.integer('channel_id').unsigned()
            table.foreign('channel_id').references('id').on('channels').on_delete('cascade')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('sms')

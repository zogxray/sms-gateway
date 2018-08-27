from orator.migrations import Migration

class ChangeChannelsTableAddSmpp(Migration):

    def up(self):
        """
        Run the migrations.
        """

        with self.schema.table('channels') as table:
            table.string('smpp_sim_id')
            table.string('smpp_sim_pass')
            table.string('smpp_sim_address')
            table.integer('smpp_sim_port').unsigned()
            table.string('protocol')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('channels') as table:
            table.drop_column('smpp_sim_id')
            table.drop_column('smpp_sim_pass')
            table.drop_column('smpp_sim_address')
            table.drop_column('smpp_sim_port')
            table.drop_column('protocol')



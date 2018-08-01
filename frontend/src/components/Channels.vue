<template>
  <div>
    <md-progress-bar md-mode="indeterminate" v-if="loading" />
    <md-empty-state v-if="error"
      class="md-accent"
      md-rounded
      md-icon="error"
      md-label="Whoops!"
      md-description="Something went wrong.">
    </md-empty-state>
    <md-table  v-if="!error" v-model="items.data" md-sort="name" md-sort-order="asc" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">{{ 'simCarts' | trans }}</h1>
        </div>

        <md-field md-clearable class="md-toolbar-section-end">
          <md-input placeholder="Поиск..." v-model="filter.text"/>
        </md-field>
      </md-table-toolbar>

      <md-table-empty-state
        md-label="No sms found"
        :md-description="`No channels found. Try a different search term.`">
      </md-table-empty-state>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Название" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell :md-label="'phone' | trans" md-sort-by="phone">{{ item.phone }}</md-table-cell>
        <md-table-cell md-label="Sim id канала" md-sort-by="sim_id">{{ item.sim_id }}</md-table-cell>
        <md-table-cell md-label="Sim ключ канала" md-sort-by="sim_pass">{{ item.sim_pass }}</md-table-cell>
        <md-table-cell md-label="Баланс" md-sort-by="balance">{{ item.balance }}</md-table-cell>
        <md-table-cell md-label="Активность" md-sort-by="last_live_at" md-tooltip="Время последней активности канала">{{ item.last_live_at | moment('timezone', 'Europe/Kiev','D-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell md-label="Дата создания" md-sort-by="created_at">{{ item.created_at | moment('timezone', 'Europe/Kiev', 'DD-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>
          <router-link :to="{ name: 'EditChannel', params: {id: item.id}}">
            Изменить
          </router-link>
        </md-table-cell>
      </md-table-row>
    </md-table>
    <pagination class="col bg-faded py-3" :data="items" :limit="items.per_page"
                v-on:pagination-change-page="getPage"></pagination>
  </div>
</template>

<script>
export default {
  name: 'Channels',
  data: () => ({
    filter: {
      text: ''
    },
    items: {
      data: []
    },
    loading: false,
    interval: null,
    error: null
  }),
  created: function () {
    let filter = JSON.parse(localStorage.getItem('channels-filter'))

    if (filter !== null) {
      this.filter = filter
    } else {
      this.getFiltered(this.$route.params.page)
    }
  },
  watch: {
    filter: {
      handler: function (val, oldVal) {
        localStorage.setItem('channels-filter', JSON.stringify(val))
        this.getFiltered(this.$route.params.page)
      },
      deep: true
    }
  },
  methods: {
    getPage: function (page) {
      if (typeof page === 'undefined') {
        self.page = 1
      } else {
        self.page = page
      }
      self.$router.push({name: 'ChannelsPage', params: {page: self.page}})
    },
    getFiltered: function (page) {
      let self = this

      if (typeof page === 'undefined') {
        self.page = 1
      } else {
        self.page = page
      }

      self.loading = true

      self.$root.axios.post('channels/' + self.page, self.filter)
        .then(function (response) {
          self.items = response.data
          self.loading = false
        })
        .catch(function (error) {
          self.error = error
          self.loading = false
        })
    }
  }
}
</script>

<style lang="scss" scoped>
  .md-progress-bar {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
  }
</style>

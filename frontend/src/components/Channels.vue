<template>
  <div>
    <md-progress-bar md-mode="indeterminate" v-if="loading" />
    <md-empty-state v-if="error"
      class="md-accent"
      md-rounded
      md-icon="error"
      :md-label="'errorLabel' | trans"
      :md-description="'errorDescription' | trans"
    >
    </md-empty-state>
    <md-table  v-if="!error" v-model="items.data" md-sort="name" md-sort-order="asc" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">{{ 'simCarts' | trans }}</h1>
        </div>

        <md-field md-clearable class="md-toolbar-section-end">
          <md-input :placeholder="'search' | trans" v-model="filter.text"/>
        </md-field>
      </md-table-toolbar>

      <md-table-empty-state
        :md-label="'notFoundLabel' | trans"
        :md-description="'notFoundDescription' | trans"
      >
      </md-table-empty-state>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell :md-label="'id' | trans" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell :md-label="'name' | trans" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell :md-label="'phone' | trans" md-sort-by="phone">{{ item.phone }}</md-table-cell>
        <md-table-cell :md-label="'sim_id' | trans" md-sort-by="sim_id">{{ item.sim_id }}</md-table-cell>
        <md-table-cell :md-label="'sim_pass' | trans" md-sort-by="sim_pass">{{ item.sim_pass }}</md-table-cell>
        <md-table-cell :md-label="'balance' | trans" md-sort-by="balance">{{ item.balance }}</md-table-cell>
        <md-table-cell :md-label="'check_balance' | trans">
          <md-button v-on:click.prevent="checkBalance(item)"
                     class="md-icon-button md-dense md-raised"
                     v-bind:class="{ 'md-accent': checkInCheckers(item), 'md-primary': !checkInCheckers(item) }"
          >
            <md-icon>cached</md-icon>
          </md-button>
        </md-table-cell>
        <md-table-cell :md-label="'last_live_at' | trans" md-sort-by="last_live_at">{{ item.last_live_at | moment('timezone', 'Europe/Kiev','D-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell :md-label="'createdAt' | trans" md-sort-by="created_at">{{ item.created_at | moment('timezone', 'Europe/Kiev', 'DD-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell :md-label="'edit' | trans">
          <router-link :to="{ name: 'EditChannel', params: {id: item.id}}">
            {{ 'edit' | trans }}
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
    checkers: [],
    loading: false,
    interval: null,
    error: null
  }),
  mounted: function () {
    let filter = JSON.parse(localStorage.getItem('channels-filter'))

    if (filter !== null) {
      this.filter = filter
    } else {
      this.getFiltered(this.$route.params.page)
    }
  },
  computed: {
    classObject: function () {
      return {
        active: this.isActive && !this.error,
        'text-danger': this.error && this.error.type === 'fatal'
      }
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

      self.$axios.post('channels/' + self.page, self.filter)
        .then(function (response) {
          self.items = response.data
          self.loading = false
        })
        .catch(function (error) {
          self.error = error
          self.loading = false
        })
    },
    checkInCheckers: function (item) {
      let it = item

      return (this.checkers.filter(e => e.id === it.id).length > 0)
    },
    checkBalance: function (item) {
      let self = this
      let it = item

      if (self.checkInCheckers(item)) {
        return
      }

      self.$axios.post('ussd/add', {
        ussd: item.balance_ussd,
        channel_id: item.id
      })
        .then(function (response) {
          let checker = {
            id: it.id,
            interval: setInterval(function () {
              self.loading = true
              self.$axios.get('channel/' + it.id)
                .then(function (response) {
                  let index = self.items.data.findIndex(e => e.id === response.data.id)
                  if (self.items.data[index].updated_at !== response.data.updated_at) {
                    let checkerIndex = self.checkers.findIndex(e => e.id === response.data.id)
                    clearInterval(self.checkers[checkerIndex].interval)
                    self.checkers.splice(checkerIndex, 1)
                    self.$set(self.items.data, index, response.data)
                    self.loading = false
                  }
                })
                .catch(function (error) {
                  self.error = error
                  self.checkers = []
                  self.loading = false
                })
            }, 1000)
          }
          self.checkers.push(checker)
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

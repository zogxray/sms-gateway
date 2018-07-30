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
    <md-table v-if="!error" v-model="items.data" md-sort="name" md-sort-order="asc" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">Входящие Sms</h1>
        </div>

        <md-field md-clearable class="md-toolbar-section-end">
          <md-input placeholder="Поиск..." v-model="filter.text"/>
        </md-field>
      </md-table-toolbar>

      <md-table-empty-state
        md-label="No sms found"
        :md-description="`No sms found. Try a different search term.`">
      </md-table-empty-state>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Телефон" md-sort-by="phone">{{ item.phone }}</md-table-cell>
        <md-table-cell md-label="Текст" md-sort-by="text">{{ item.text }}</md-table-cell>
        <md-table-cell md-label="Sim карта" md-sort-by="channel_id">{{ item.channel.name }}</md-table-cell>
        <md-table-cell md-label="Дата получения" md-sort-by="created_at">{{ item.created_at | moment('timezone', 'Europe/Kiev', 'D-MM-YYYY HH:mm:ss') }}</md-table-cell>
      </md-table-row>
    </md-table>
    <pagination class="col bg-faded py-3" :data="items" :limit="items.per_page"
                v-on:pagination-change-page="getPage"></pagination>
    <audio id="tick" src="/static/audio/tick.mp3"></audio>
  </div>
</template>

<script>
export default {
  name: 'IncomingSms',
  data: () => ({
    filter: {
      text: ''
    },
    items: {
      data: []
    },
    loading: false,
    error: null,
    interval: null
  }),
  created: function () {
    let filter = JSON.parse(localStorage.getItem('incoming-sms-filter'))

    if (filter !== null) {
      this.filter = filter
    } else {
      this.getFiltered(this.$route.params.page)
    }
  },
  watch: {
    filter: {
      handler: function (val, oldVal) {
        localStorage.setItem('incoming-sms-filter', JSON.stringify(val))
        this.getFiltered(this.$route.params.page)
      },
      deep: true
    }
  },
  beforeDestroy: function () {
    clearInterval(this.interval)
  },
  methods: {
    getPage: function (page) {
      if (typeof page === 'undefined') {
        self.page = 1
      } else {
        self.page = page
      }
      this.$router.push({name: 'IncomingSms', params: {page: self.page}})
    },
    getFiltered: function (page) {
      let self = this

      if (typeof page === 'undefined') {
        self.page = 1
      } else {
        self.page = page
      }

      self.loading = true

      self.$root.axios.post('incoming-sms/' + self.page, self.filter)
        .then(function (response) {
          self.items = response.data
          self.loading = false
          if (self.page === 1) {
            if (self.interval !== null) {
              clearInterval(self.interval)
            }
            self.interval = setInterval(function () {
              self.$root.axios.post('incoming-sms/latest', {date: self.items.data[0].created_at})
                .then(function (response) {
                  if (response.data !== null) {
                    self.items.data.unshift(response.data)
                    self.items.data.pop()

                    let audio = document.getElementById('tick')
                    audio.play()
                  }
                })
                .catch(function (error) {
                  self.error = error
                  self.loading = false
                })
            }, 5000)
          }
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
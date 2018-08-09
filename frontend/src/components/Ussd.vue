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
    <md-table v-if="!error" v-model="items.data" md-sort="name" md-sort-order="asc" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">{{ 'ussd' | trans }}</h1>
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
        <md-table-cell :md-label="'ussdRequest' | trans" md-sort-by="ussd">{{ item.ussd }}</md-table-cell>
        <md-table-cell :md-label="'ussdAnswer' | trans" md-sort-by="answer">{{ item.answer }}</md-table-cell>
        <md-table-cell :md-label="'simCart' | trans" md-sort-by="channel_id">{{ item.channel.name }}</md-table-cell>
        <md-table-cell :md-label="'requestSentAt' | trans" md-sort-by="send_at">{{ item.send_at | moment('timezone', 'Europe/Kiev', 'DD-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell :md-label="'requestReceivedAt' | trans" md-sort-by="received_at">{{ item.received_at | moment('timezone', 'Europe/Kiev', 'DD-MM-YYYY HH:mm:ss') }}</md-table-cell>
        <md-table-cell :md-label="'createdAt' | trans" md-sort-by="created_at">{{ item.created_at | moment('timezone', 'Europe/Kiev', 'DD-MM-YYYY HH:mm:ss') }}</md-table-cell>
      </md-table-row>
    </md-table>
    <pagination class="col bg-faded py-3" :data="items" :limit="items.per_page"
                v-on:pagination-change-page="getPage"></pagination>
  </div>
</template>

<script>
export default {
  name: 'Ussd',
  data: () => ({
    filter: {
      text: ''
    },
    items: {
      data: []
    },
    loading: false,
    error: null
  }),
  created: function () {
    let filter = JSON.parse(localStorage.getItem('ussd-filter'))

    if (filter !== null) {
      this.filter = filter
    } else {
      this.getFiltered(this.$route.params.page)
    }
  },
  watch: {
    filter: {
      handler: function (val, oldVal) {
        localStorage.setItem('ussd-filter', JSON.stringify(val))
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
      this.$router.push({name: 'Ussd', params: {page: self.page}})
    },
    getFiltered: function (page) {
      let self = this

      if (typeof page === 'undefined') {
        self.page = 1
      } else {
        self.page = page
      }

      self.loading = true

      self.$axios.post('ussd/' + self.page, self.filter)
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

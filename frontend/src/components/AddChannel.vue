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
    <form v-if="!error" novalidate class="md-layout" @submit.prevent="validateItem">
      <md-card class="md-layout-item md-size-100 md-small-size-100">
        <md-card-header>
          <div class="md-title">{{ 'addSim' | trans }}</div>
        </md-card-header>

        <md-toolbar class="md-accent">
          <p>Передающий канал должен быть настроен на GoIP устройстве. Поле активность в списке каналов покажет дату последнего запроса с утройства</p>
        </md-toolbar>

        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-10name0">
              <md-field :class="getValidationClass('name')">
                <label for="name">Название</label>
                <md-input name="name" id="name" autocomplete="given-name" v-model="form.name" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.name.required">Название обязательно для заполнения</span>
              </md-field>
              <md-field :class="getValidationClass('sim_id')">
                <label for="sim-id">SIM-канал ID</label>
                <md-input name="sim-id" id="sim-id" autocomplete="given-sim-id" v-model="form.sim_id" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.sim_id.required">ID обязателен для заполнения</span>
              </md-field>
              <md-field :class="getValidationClass('sim_pass')">
                <label for="sim-pass">SIM-канал ключ</label>
                <md-input name="sim-pass" id="sim-pass" autocomplete="given-sim-pass" v-model="form.sim_pass" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.sim_pass.required">Ключ обязателен для заполнения</span>
              </md-field>
              <md-field :class="getValidationClass('phone')">
                <label for="sim-phone">SIM-канал телефон</label>
                <md-input name="sim-phone" id="sim-phone" autocomplete="given-sim-phone" v-model="form.phone" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.phone.required">Телефон обязателен для заполнения</span>
              </md-field>
              <md-field :class="getValidationClass('balance_ussd')">
                <label for="sim-balance">USSD-код проверки баланса</label>
                <md-input name="sim-balance" id="sim-balance" autocomplete="given-sim-balance" v-model="form.balance_ussd" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.balance_ussd.required">USSD-код проверки баланса обязателен для заполнения</span>
              </md-field>
            </div>
          </div>
        </md-card-content>
        <md-card-actions>
          <md-button v-if="id" type="submit" class="md-primary" :disabled="loading">{{ 'updateSim' | trans }}</md-button>
          <md-button v-if="!id" type="submit" class="md-primary" :disabled="loading">{{ 'addSim' | trans }}</md-button>
        </md-card-actions>
      </md-card>
    </form>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import {
  required
} from 'vuelidate/lib/validators'
export default {
  name: 'AddChannel',
  mixins: [validationMixin],
  data: () => ({
    form: {
      name: null,
      sim_id: null,
      sim_pass: null,
      phone: null,
      balance_ussd: null
    },
    id: null,
    loading: false,
    error: null
  }),
  validations: {
    form: {
      name: {
        required
      },
      sim_id: {
        required
      },
      sim_pass: {
        required
      },
      phone: {
        required
      },
      balance_ussd: {
        required
      }
    }
  },
  created: function () {
    this.id = this.$route.params.id

    if (this.id !== null) {
      this.getItem()
    }
  },
  methods: {
    getValidationClass: function (fieldName) {
      const field = this.$v.form[fieldName]

      if (field) {
        return {
          'md-invalid': field.$invalid && field.$dirty
        }
      }
    },
    getItem: function () {
      let self = this
      self.$root.axios.get('channels/' + self.id + '/edit')
        .then(function (response) {
          self.form = {
            name: response.data.name,
            sim_id: response.data.sim_id,
            sim_pass: response.data.sim_pass,
            phone: response.data.phone,
            balance_ussd: response.data.balance_ussd
          }
          self.loading = false
        })
        .catch(function (error) {
          self.error = error
          self.loading = false
        })
    },
    saveItem: function () {
      let self = this
      self.loading = true

      let route = ''

      if (self.id !== 'undefined') {
        route = 'channels/' + self.id + '/update'
      } else {
        route = 'channels/add'
      }

      self.$root.axios.post(route, self.form)
        .then(function (response) {
          self.items = response.data
          self.loading = false
          self.$router.push({name: 'Channels'})
        })
        .catch(function (error) {
          self.error = error
          self.loading = false
        })
    },
    validateItem: function () {
      this.$v.$touch()

      if (!this.$v.$invalid) {
        this.saveItem()
      }
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

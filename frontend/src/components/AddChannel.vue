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
          <p>{{ 'channel_warring' | trans }}</p>
        </md-toolbar>

        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-10name0">
              <md-field :class="getValidationClass('name')">
                <label for="name">{{ 'name' | trans }}</label>
                <md-input name="name" id="name" autocomplete="given-name" v-model="form.name" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.name.required">{{ 'form.name.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('sim_id')">
                <label for="sim-id">{{ 'sim_id' | trans }}</label>
                <md-input name="sim-id" id="sim-id" autocomplete="given-sim-id" v-model="form.sim_id" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.sim_id.required">{{ 'form.sim_id.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('sim_pass')">
                <label for="sim-pass">{{ 'sim_pass' | trans }}</label>
                <md-input name="sim-pass" id="sim-pass" autocomplete="given-sim-pass" v-model="form.sim_pass" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.sim_pass.required">{{ 'form.sim_pass.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('smpp_sim_id')">
                <label for="smpp_sim_id">{{ 'smpp_sim_id' | trans }}</label>
                <md-input name="sim-id" id="smpp_sim_id" autocomplete="given-smpp_sim_id" v-model="form.smpp_sim_id" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.smpp_sim_id.required">{{ 'form.smpp_sim_id.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('smpp_sim_pass')">
                <label for="smpp_sim_pass">{{ 'smpp_sim_pass' | trans }}</label>
                <md-input name="smpp_sim_pass" id="smpp_sim_pass" autocomplete="given-smpp_sim_pass" v-model="form.smpp_sim_pass" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.smpp_sim_pass.required">{{ 'form.smpp_sim_pass.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('smpp_sim_address')">
                <label for="smpp_sim_address">{{ 'smpp_sim_address' | trans }}</label>
                <md-input name="sim-id" id="smpp_sim_address" autocomplete="given-smpp_sim_address" v-model="form.smpp_sim_address" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.smpp_sim_address.required">{{ 'form.smpp_sim_address.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('smpp_sim_port')">
                <label for="smpp_sim_port">{{ 'smpp_sim_port' | trans }}</label>
                <md-input name="smpp_sim_port" id="smpp_sim_port" autocomplete="given-smpp_sim_port" v-model="form.smpp_sim_port" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.smpp_sim_port.required">{{ 'form.smpp_sim_port.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('phone')">
                <label for="sim-phone">{{ 'phone' | trans }}</label>
                <md-input name="sim-phone" id="sim-phone" autocomplete="given-sim-phone" v-model="form.phone" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.phone.required">{{ 'form.phone.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('balance_ussd')">
                <label for="sim-balance">{{ 'ussd_balance' | trans }}</label>
                <md-input name="sim-balance" id="sim-balance" autocomplete="given-sim-balance" v-model="form.balance_ussd" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.balance_ussd.required">{{ 'form.balance_ussd.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('protocol')">
                <label for="protocol">{{'protocol' | trans}}</label>
                <md-select name="protocol" id="protocol" v-model="form.protocol" md-dense :disabled="loading">
                  <md-option v-for="protocol in protocols" v-bind:key="protocol.id" v-bind:value="protocol.id">{{protocol.name}}</md-option>
                </md-select>
                <span class="md-error" v-if="!$v.form.protocol.required">{{'form.protocol.required' | trans}}</span>
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
      smpp_sim_id: null,
      smpp_sim_pass: null,
      smpp_sim_address: null,
      smpp_sim_port: null,
      phone: null,
      balance_ussd: null,
      protocol: null,
    },
    protocols: [
      {'id': 'goip', name: 'GOIP'},
      {'id': 'smpp', name: 'SMPP'}
    ],
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
      smpp_sim_id: {
        required
      },
      smpp_sim_pass: {
        required
      },
      smpp_sim_address: {
        required
      },
      smpp_sim_port: {
        required
      },
      phone: {
        required
      },
      balance_ussd: {
        required
      },
      protocol: {
        required
      }
    }
  },
  mounted: function () {
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
      self.$axios.get('channel/' + self.id)
        .then(function (response) {
          self.form = {
            name: response.data.name,
            sim_id: response.data.sim_id,
            sim_pass: response.data.sim_pass,
            smpp_sim_id: response.data.smpp_sim_id,
            smpp_sim_pass: response.data.smpp_sim_pass,
            smpp_sim_address: response.data.smpp_sim_address,
            smpp_sim_port: response.data.smpp_sim_port,
            protocol: response.data.protocol,
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

      self.$axios.post(route, self.form)
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

<template>
  <div>
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
          <div class="md-title">{{ 'sendSms' | trans }}</div>
        </md-card-header>
        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-10name0">
              <md-field :class="getValidationClass('phone')">
                <label for="phone">{{ 'phone' | trans }}</label>
                <md-input name="phone" id="phone" autocomplete="given-phone" v-model="form.phone" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.phone.required">{{ 'form.phone.required' | trans }}</span>
              </md-field>
              <md-field :class="getValidationClass('text')">
                <label for="text">{{'text' | trans}}</label>
                <md-input name="text" id="text" autocomplete="given-text" v-model="form.text" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.text.required">{{'form.text.required' | trans}}</span>
              </md-field>
              <md-field :class="getValidationClass('channel_id')">
                <label for="channel-id">{{'channel_id' | trans}}</label>
                <md-select name="channel-id" id="channel-id" v-model="form.channel_id" md-dense :disabled="loading">
                  <md-option v-for="channel in channels" v-bind:key="channel.id" v-bind:value="channel.id">{{channel.name}}</md-option>
                </md-select>
                <span class="md-error" v-if="!$v.form.channel_id.required">{{'form.channel_id.required' | trans}}</span>
              </md-field>
            </div>
          </div>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="loading" />

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="loading">{{ 'sendSms' | trans }}</md-button>
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
  name: 'SendSms',
  mixins: [validationMixin],
  data: () => ({
    form: {
      phone: null,
      text: null,
      channel_id: null
    },
    channels: [],
    loading: false,
    error: null
  }),
  validations: {
    form: {
      phone: {
        required
      },
      text: {
        required
      },
      channel_id: {
        required
      }
    }
  },
  mounted: function () {
    this.getChannels()
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
    getChannels: function () {
      let self = this
      self.$axios.get('channels/all')
        .then(function (response) {
          self.channels = response.data
        })
        .catch(function (error) {
          self.error = error
          self.loading = false
        })
    },
    saveItem: function () {
      let self = this
      self.loading = true
      self.$axios.post('outgoing-sms/add', self.form)
        .then(function (response) {
          self.items = response.data
          self.loading = false
          self.$router.push({name: 'OutgoingSms'})
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

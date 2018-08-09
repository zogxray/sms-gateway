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
          <div class="md-title">Login</div>
        </md-card-header>

        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('login')">
                <label for="login">Login</label>
                <md-input name="login" id="login" autocomplete="given-login" v-model="form.login" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.login.required">Login is required</span>
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('password')">
                <label for="password">Password</label>
                <md-input name="password" id="password" type="password" v-model="form.password" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.password.required">Password is required</span>
              </md-field>
            </div>
          </div>
        </md-card-content>

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="loading">Login</md-button>
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
  name: 'Login',
  mixins: [validationMixin],
  data: () => ({
    form: {
      login: null,
      password: null
    },
    loading: false,
    error: null
  }),
  validations: {
    form: {
      login: {
        required
      },
      password: {
        required
      }
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
    saveItem: function () {
      let self = this
      self.loading = true

      self.$axios.post('login', self.form)
        .then(function (response) {
          self.items = response.data
          self.$root.auth.token = response.data.token
          self.loading = false
          self.$router.push({name: 'IncomingSms'})
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

<style scoped>

</style>

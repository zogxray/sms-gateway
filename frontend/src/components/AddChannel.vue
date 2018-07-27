<template>
  <div>
    <form novalidate class="md-layout" @submit.prevent="validateItem">
      <md-card class="md-layout-item md-size-100 md-small-size-100">
        <md-card-header>
          <div class="md-title">SIM-канал</div>
        </md-card-header>

        <md-toolbar class="md-accent">
          <p>При добавлении канала важно понимать, что передающий канал должен быть настроен на GoIP устройстве. Поле активность в списке каналов покажет дату последнего запроса с утройства</p>
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
                <label for="name">SIM-канал телефон</label>
                <md-input name="sim-phone" id="sim-phone" autocomplete="given-sim-phone" v-model="form.phone" :disabled="loading" />
                <span class="md-error" v-if="!$v.form.phone.required">Телефон обязателен для заполнения</span>
              </md-field>
            </div>
          </div>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="loading" />

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="loading">Добавить канал</md-button>
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
      phone: null
    },
    loading: false
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

      self.$root.axios.post('channels/add', self.form)
        .then(function (response) {
          self.items = response.data
          self.loading = false
          self.$router.push({name: 'Channels'})
        })
        .catch(function (error) {
          console.log(error)
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

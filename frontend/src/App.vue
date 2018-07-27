<template>
  <div class="page-container">
    <md-app>
      <md-app-drawer md-permanent="full">
        <md-toolbar class="md-transparent" md-elevation="0">
          <h2>SMS - шлюз</h2>
        </md-toolbar>

        <md-list>
          <router-link :to="{ name: 'Sms'}" tag="md-list-item">
            <md-icon>move_to_inbox</md-icon>
            <span class="md-list-item-text">Входящие Sms</span>
          </router-link>

          <router-link :to="{ name: 'Channels'}" tag="md-list-item">
            <md-icon>menu</md-icon>
            <span class="md-list-item-text">SIM карты</span>
          </router-link>

          <router-link :to="{ name: 'AddChannel'}" tag="md-list-item">
            <md-icon>add</md-icon>
            <span class="md-list-item-text">Добавить SIM</span>
          </router-link>

        </md-list>
      </md-app-drawer>

      <md-app-content>
        <router-view :key="$route.fullPath"></router-view>
      </md-app-content>
    </md-app>
  </div>
</template>

<style lang="scss">
  @import '~bootstrap/scss/bootstrap';

  .md-app {
    border: 1px solid rgba(#000, .12);
  }

  // Demo purposes only
  .md-drawer {
    width: 230px;
    max-width: calc(100vw - 125px);
  }
</style>

<script>
export default {
  name: 'App'
}
</script>

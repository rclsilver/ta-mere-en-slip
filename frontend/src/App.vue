<template>
  <v-app>
    <v-container app fill-height>
      <v-row v-if="!game">
        <v-col cols="12" sm="6">
          <create-game />
        </v-col>
        <v-col cols="12" sm="6">
          <join-game />
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col cols="12">
          <game />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import CreateGame from './components/CreateGame.vue'
import JoinGame from './components/JoinGame.vue'
import Game from './components/Game.vue'

export default {
  name: 'app',
  components: {
    CreateGame,
    JoinGame,
    Game
  },
  computed: {
    game () {
      return this.$store.state.settings.game_id
    }
  },
  mounted () {
    this.$store.dispatch('settings/load', this)
  }
}
</script>

<style>
  html, body {
    margin: 0;
    background: #f1f1f1;
  }
</style>

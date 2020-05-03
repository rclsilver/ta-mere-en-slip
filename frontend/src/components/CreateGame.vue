<template>
  <v-card>
    <v-card-title>Nouvelle partie</v-card-title>
    <v-card-text>
      <v-text-field
        label="Ton nom"
        v-model="name"
      ></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-btn :disabled="!name" @click="createGame()">Créer une partie</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Game',

  computed: {
    name: {
      get () {
        return this.$store.state.settings.name
      },
      set (value) {
        this.$store.dispatch('settings/name', value)
      }
    }
  },

  methods: {
    createGame () {
      this.$api.game.create(this.name).then((r) => {
        this.$store.dispatch('settings/playerId', r.data.id)
        this.$store.dispatch('settings/gameId', r.data.game)
      })
    }
  }
}
</script>

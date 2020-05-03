<template>
  <v-card>
    <v-card-title>Rejoindre une partie</v-card-title>
    <v-card-text>
      <v-text-field
        label="Ton nom"
        v-model="name"
      ></v-text-field>
      <v-text-field
        label="Code de la partie"
        v-model="secret"
      ></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-btn :disabled="!name || !secret" @click="joinGame()">Rejoindre une partie</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Game',

  data () {
    return {
      secret: undefined
    }
  },

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
    joinGame () {
      this.$api.game.join(this.name, this.secret).then((r) => {
        this.$store.dispatch('settings/playerId', r.data.id)
        this.$store.dispatch('settings/gameId', r.data.game)
      })
    }
  }
}
</script>

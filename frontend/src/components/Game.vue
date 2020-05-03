<template>
  <v-card v-if="data">
    <v-card-title v-if="waiting">En attente de joueurs...</v-card-title>
    <v-card-title v-else>Au tour de {{ data.current_player.name }}</v-card-title>
    <v-card-text v-if="waiting">
      <p class="secret">{{ data.secret }}</p>
      <div class="players">
        <p>Liste des joueurs :</p>
        <ul>
          <li v-for="player in data.players" :key="player.id">{{ player.name }}</li>
        </ul>
      </div>
    </v-card-text>
    <v-card-text v-else>
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" class="card character">
            {{ (playerId !== currentPlayerId) || data.current_player.character_found ? data.current_player.character.text : '?' }}
          </v-col>
          <v-col cols="12" sm="6" class="card action">
            {{ (playerId !== currentPlayerId) || data.current_player.action_found ? data.current_player.action.text : '?' }}
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
    <v-card-actions v-if="waiting">
      <v-btn v-on:click="startGame()">Démarre la partie</v-btn>
    </v-card-actions>
    <v-card-actions v-else>
      <v-container>
        <v-row>
          <v-col cols="12" sm="4">
            <v-btn v-if="foundCharacterButton" @click="nextPlayer(true, false)">Personnage trouvé</v-btn>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn v-if="foundActionButton" @click="nextPlayer(false, true)">Action trouvée</v-btn>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn @click="nextPlayer(false, false)">Joueur suivant</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Game',

  data () {
    return {
      ticker: null,
      data: undefined
    }
  },

  created () {
    this.ticker = setInterval(() => {
      if (this.game) {
        this.$api.game.get(this.game).then((r) => {
          if (r.data.finished) {
            this.finishGame()
          } else {
            this.data = r.data
          }
        }).catch((e) => {
          this.finishGame()
        })
      }
    }, 1000)
  },

  destroyed () {
    if (this.ticker) {
      clearInterval(this.ticker)
    }
  },

  computed: {
    game () {
      return this.$store.state.settings.game_id
    },
    playerId () {
      return this.$store.state.settings.player_id
    },
    currentPlayerId () {
      if (this.data && this.data.current_player) {
        return this.data.current_player.id
      } else {
        return undefined
      }
    },
    foundCharacterButton () {
      return this.playerId !== this.currentPlayerId && !this.data.current_player.character_found
    },
    foundActionButton () {
      return this.playerId !== this.currentPlayerId && !this.data.current_player.action_found
    },
    waiting () {
      return this.data && !this.data.started
    }
  },

  methods: {
    startGame () {
      const options = {
        title: 'Start the game',
        icon: 'warning',
        buttonTrueText: 'Yes, start the game!'
      }

      this.$confirm(`Are you sure to start the game?`, options).then(res => {
        if (res) {
          this.$api.game.start(this.game).catch((e) => {
            alert('Unable to start the game: ' + e.response.data.error)
          })
        }
      })
    },
    finishGame () {
      this.$store.dispatch('settings/gameId', undefined)
      this.$store.dispatch('settings/playerId', undefined)
    },
    nextPlayer (foundCharacter, foundAction) {
      const options = {
        title: 'Next player',
        icon: 'warning',
        buttonTrueText: 'Yes, next player!'
      }

      this.$confirm(`Are you sure?`, options).then(res => {
        if (res) {
          this.$api.game.nextPlayer(this.game, this.data.current_player.id, foundCharacter, foundAction)
        }
      })
    }
  }
}
</script>

<style scoped>
button {
  width: 100%;
}

.card {
  border: 10px solid;
  font-weight: bold;
  font-size: 24px;
  text-align: center;
}

.character {
  border-color: rgb(2, 79, 151);
}

.action {
  border-color: rgb(230, 40, 173);
}
</style>

function loadSettings () {
  try {
    return JSON.parse(localStorage.getItem('tmes')) || {}
  } catch (e) {
    return {}
  }
}

function saveSettings (settings) {
  localStorage.setItem('tmes', JSON.stringify(settings))
}

export default {
  namespaced: true,
  state: {
    game_id: undefined,
    player_id: undefined,
    name: undefined
  },
  actions: {
    load ({ commit }) {
      const settings = loadSettings()

      commit('setGameId', settings.game_id)
      commit('setPlayerId', settings.player_id)
      commit('setName', settings.name)
    },
    gameId ({ commit }, gameId) {
      commit('setGameId', gameId)
    },
    playerId ({ commit }, playerId) {
      commit('setPlayerId', playerId)
    },
    name ({ commit }, name) {
      commit('setName', name)
    }
  },
  mutations: {
    setGameId (state, gameId) {
      state.game_id = gameId
      saveSettings(state)
    },
    setPlayerId (state, playerId) {
      state.player_id = playerId
      saveSettings(state)
    },
    setName (state, name) {
      state.name = name
      saveSettings(state)
    }
  }
}

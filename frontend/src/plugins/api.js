import axios from 'axios'

export default {
  install (Vue, store) {
    if (!store) {
      throw new Error('Need to be used with Vuex Sotre')
    }

    const config = {
      baseURL: process.env.VUE_APP_API_URL || '',
      headers: {
        'Content-Type': 'application/json'
      }
    }

    const client = axios.create(config)

    Vue.prototype.$api = {
      $url: config.baseURL,
      game: {
        create: (name) => client.post('/api/games/create', { name }),
        join: (name, secret) => client.post('/api/games/join', { name, secret }),
        get: (id) => client.get(`/api/games/${id}`, {
          headers: {
            'Player-Id': store.state.settings.player_id
          }
        }),
        start: (id) => client.post(`/api/games/${id}/start`, {}, {
          headers: {
            'Player-Id': store.state.settings.player_id
          }
        }),
        nextPlayer: (id, currentPlayer, characterFound, actionFound) => client.post(`/api/games/${id}/next-player`, { current_player: currentPlayer, character_found: characterFound, action_found: actionFound }, {
          headers: {
            'Player-Id': store.state.settings.player_id
          }
        })
      }
    }
  }
}

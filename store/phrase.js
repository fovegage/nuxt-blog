import { SET_PHRASE_LIST } from './mutations-types'
import site from '../nuxt.config'

export const state = () => ({
  list: []
})

export const mutations = {
  [SET_PHRASE_LIST] (state, data) {
    state.list = data
  }
}

export const actions = {
  async getPhraseList ({ commit }) {
    try {
      let { data } = await this.$axios.get(`${process.env.baseUrl}/say`, {
        type: site.site.type
      })
      commit(SET_PHRASE_LIST, data.data)
      return Promise.resolve(data.data)
    } catch (error) {
      return Promise.reject(error)
    }
  }
}

export default {
    updateAccessToken ({ commit }, token) {
        localStorage.token = token
        commit('updateAccessToken', token)
    },
    updateLoggedUserEmail ({ commit }, email) {
        localStorage.logged_user_email = email
        commit('updateLoggedUserEmail', email)
    },
    updateUserRole ({ commit }, role) {
        localStorage.role = role
        commit('updateUserRole', role)
    }
}
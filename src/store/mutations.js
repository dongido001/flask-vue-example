export default {
    increment (state) {
        state.count++
    },
    updateAccessToken(state, token) {
        state.token = token
        localStorage.token = token
    },
    updateLoggedUserEmail(state, email) {
       state.logged_user_email = email
    }
}
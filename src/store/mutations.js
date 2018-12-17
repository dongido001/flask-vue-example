export default {
    updateAccessToken(state, token) {
        state.token = token
    },
    updateLoggedUserEmail(state, email) {
       state.logged_user_email = email
    },
    updateUserRole(state, role) {
        state.role = role
     }
}
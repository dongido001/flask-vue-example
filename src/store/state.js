export default {
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    logged_user_email: localStorage.getItem('logged_user_email') || null,
}
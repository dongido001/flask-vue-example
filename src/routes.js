import Dashboard from './components/Dashboard'
import Login from './components/Login'

const routes = [
    { path: '/', component: Dashboard},
    { path: '/login', component: Login }
]

const publicPages = ['/login']

export {routes, publicPages};
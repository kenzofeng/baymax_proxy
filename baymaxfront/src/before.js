import router from './router'
import store from './store'

router.beforeEach((to, from, next) => {
    let project = store.getters.getproject
    if (project !== '') {
        let p = to.path
        if (p === '/project/index') {
            next({ name: 'toproject', params: { name: project } })
        } else if (p === '/lab/index') {
            next({ name: 'labtoproject', params: { name: project } })
        } else if (p === '/job/index' && to.query.project === undefined) {
            next({ path: '/job/index', query: { number: 30, project: project } })
        } else if (p === '/server/index' && to.query.project === undefined) {
            next({ path: '/server/index', query: { project: project } })
        } else {
            next()
        }
    } else {
        next()
    }
})
router.afterEach(() => {})
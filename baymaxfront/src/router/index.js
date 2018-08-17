import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/views/layout'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/404', component: () => import('@/views/404'), hidden: true },
    {
      path: '/',
      component: Layout,
      redirect: '/project'
    },
    {
      path: '/project',
      name: 'Project',
      component: Layout,
      redirect: '/project/index',
      menu: true,
      children: [{
        path: 'index',
        component: () => import('@/views/project/index'),
        children: [{
          path: ':name',
          component: () => import('@/views/project/detail')
        }]

      }]
    },
    {
      path: '/lab',
      name: 'Lab',
      component: Layout,
      menu: true
    },
    {
      path: '/job',
      name: 'Job',
      component: Layout,
      menu: true
    },
    { path: '*', redirect: '/404', hidden: true }
  ]
})

import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/views/layout'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [{
    path: '/404',
    component: () =>
        import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/project'
  },
  {
    path: '/project',
    name: 'Project',
    icon: 'clipboard list',
    component: Layout,
    redirect: '/project/index',
    menu: true,
    children: [{
      path: 'index',
      component: () =>
          import('@/views/project/index'),
      children: [{
        name: 'toproject',
        path: ':name',
        component: () =>
            import('@/views/project/detail')
      }]

    }]
  },
  {
    path: '/lab',
    name: 'Lab',
    icon: 'flask',
    component: Layout,
    redirect: '/lab/index',
    menu: true,
    children: [{
      path: 'index',
      component: () =>
          import('@/views/lab/index'),
      children: [{
        path: ':name',
        name: 'labtoproject',
        component: () =>
            import('@/views/lab/index')
      }]
    }]
  },
  {
    path: '/job',
    name: 'Job',
    component: Layout,
    icon: 'tasks',
    redirect: {
      path: '/job/index',
      query: {
        number: 30
      }
    },
    menu: true,
    children: [{
      path: 'index',
      name: 'jobindex',
      component: () =>
          import('@/views/job/index'),
      children: [{
        path: ':name',
        name: 'jobtoproject',
        component: () =>
            import('@/views/job/index')
      }]
    }]
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
  ]
})

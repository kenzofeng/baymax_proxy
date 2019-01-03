<template>
  <div class="ui teal inverted huge menu">
    <navitem v-for="router in routes" :key=" router.name" :item="router"></navitem>
    <div class="right menu">
      <div class="ui right aligned category search item">
      <div class="ui transparent icon input">
        <drop :items="selectitems" @changeselected="changeselected"></drop>
      </div>
    </div>
    <a class="item" target='_blank' href="http://10.200.106.2:8080/"><i class="large jenkins icon"></i></a>
    <a class="item" target='_blank' href="http://52.34.81.222/"><i class="large gitlab icon"></i></a>
    <a class="item" target='_blank' href="http://35.160.71.185/aws?account=sandbox-test&region=us-west-2&search=Function"><i class="cloud icon"></i></a>
    <a class="item" target='_blank' href="http://54.218.22.41/"><i class="wrench icon"></i></a>
    <a class="item" target='_blank' href="https://warrior.testrail.io/index.php?/dashboard"><i class="industry icon"></i></a>
  </div>
  </div>
</template>

<script>
import navitem from './navitem'
import drop from '@/components/dropdown'
import {getList} from '@/api/project'
export default {
  name: 'navbar',
  data () {
    return {
      selectitems: []
    }
  },
  created () {
    this.fetchData()
  },
  components: {navitem, drop},
  computed: {
    routes () {
      return this.$router.options.routes
    }
  },
  methods: {
    fetchData () {
      getList(null).then(response => {
        this.selectitems = response.data
      })
    },
    changeselected (project) {
      let p = this.$route.fullPath.split('/')[1]
      this.$store.dispatch('setProjectName', project)
      if (project !== '') {
        if (p === 'project') {
          this.$router.push({name: 'toproject', params: {name: project}})
        } else if (p === 'lab') {
          this.$router.push({name: 'labtoproject', params: {name: project}})
        } else if (p === 'job') {
          this.$router.push({path: '/job/index', query: {number: 30, project: project}})
        }
      } else {
        if (p === 'lab') {
          this.$router.push({path: '/lab/index'})
        } else if (p === 'job') {
          this.$router.push({path: '/job/index', query: {number: 30}})
        }
      }
    }
  }
}
</script>

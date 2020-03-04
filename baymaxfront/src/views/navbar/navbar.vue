<template>
  <div class="ui teal huge inverted menu">
    <navitem v-for="router in routes" :key=" router.name" :item="router"></navitem>
    <div class="right menu">
      <div class="ui right aligned category search item">
        <div class="ui transparent icon input">
          <drop :items="selectitems" @changeselected="changeselected"></drop>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navitem from './navitem'
import drop from '@/components/dropdown'
import { getList } from '@/api/project'
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
  components: { navitem, drop },
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
          this.$router.push({ name: 'toproject', params: { name: project } })
        } else if (p === 'lab') {
          this.$router.push({
            name: 'labtoproject',
            params: { name: project }
          })
        } else if (p === 'job') {
          this.$router.push({
            path: '/job/index',
            query: { number: 30, project: project }
          })
        } else if (p === 'server') {
          this.$router.push({
            path: '/server/index',
            query: { project: project }
          })
        }
      } else {
        if (p === 'lab') {
          this.$router.push({ path: '/lab/index' })
        } else if (p === 'job') {
          this.$router.push({ path: '/job/index', query: { number: 30 } })
        } else if (p === 'server') {
          this.$router.push({ path: '/server/index', query: { number: 30 } })
        }
      }
    }
  }
}
</script>

<template>
  <div>
    <table class="ui compact selectable celled striped teal table">
      <thead>
        <tr>
          <th class="two wide">Project</th>
          <th class="one wide">Servers</th>
          <th>Test Automation</th>
          <th class="one wide">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tp in projects" :key="tp.name">
          <td>{{tp.name}}</td>
          <td>
              <div class="ui aligned divided list">
                <a class="item" v-for="node in tp.nodes" :key="node">
                <i class="orange server icon"></i>
                <div class="content">
                    <div class="header">{{node}}</div>
                </div>
                </a>
            </div>
          </td>
          <td>
            <table class="ui small table very compact">
              <thead>
                <th class="two wide">Test</th>
                <th class="nine wide">URL</th>
                <th>Robot Parameter</th>
              </thead>
              <tbody>
                <tr v-for="map in tp.maps" :key="map.test">
                  <td>{{map.test}}</td>
                  <td>{{map.testurl}}</td>
                  <td>{{map.robot_parameter}}</td>
                </tr>
              </tbody>
            </table>
          </td>
          <td class="center aligned">
              <button class="ui icon button blue" @click="runshow(tp)">
                <i class="play icon"></i>
                </button>
          </td>
        </tr>
      </tbody>
    </table>
    <model  ref="runmodelcomponent" @yes="runproject" :name="run">
      <div slot="header">Run Project</div>
      <div slot="content">Are you sure run project?</div>
    </model>
    <model  ref="jobmodelcomponent" @yes="tojob" :name="job" >
      <div slot="header">Status</div>
      <div slot="content">{{response}}</div>
    </model>
  </div>
</template>
<script>
import model from '@/components/model'
import {getList} from '@/api/lab'
import {startjob} from '@/api/job'
export default {
  name: 'lab',
  components: {
    model
  },
  data () {
    return {
      projects: [],
      run: 'run',
      job: 'job',
      project: this.$route.params.name,
      runitem: '',
      response: ''
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    filterproject () {
      if (typeof (this.project) !== 'undefined') {
        for (let p in this.projects) {
          if (this.projects[p].name === this.project) {
            this.projects = [this.projects[p]]
            break
          }
        }
      }
    },
    fetchData () {
      getList(this.params).then(response => {
        this.projects = response.data
        this.filterproject()
      })
    },
    runshow (tp) {
      this.runitem = tp.name
      this.$refs.runmodelcomponent.$emit('show')
    },
    runproject () {
      startjob(this.runitem).then(response => {
        this.response = response.data
      })

      this.$refs.jobmodelcomponent.$emit('show')
    },
    tojob () {
      this.$router.push({path: '/job/index', query: {number: 30, project: this.runitem}})
    }
  }
}

</script>

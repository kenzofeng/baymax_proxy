<template>
  <div class="dimmable">
    <div class="ui inverted dimmer" :class="active">
      <div class="ui loader"></div>
    </div>
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
          <td @click="toproject(tp.name)"><i class="clipboard list link icon" ></i>{{tp.name}}</td>
          <td>
              <div class="ui aligned divided list">
                <div class="item" v-for="node in tp.nodes" :key="node" >
                <i :class="iconcss(node)" class="server icon"></i>
                <div class="content">
                    <div class="header">{{node}}</div>
                </div>
                </div>
            </div>
          </td>
          <td>
            <table class="ui small table very compact">
              <thead>
                <th class="two wide">Test</th>
                <th class="one wide">Type</th>
                <th class="five wide">URL</th>
                <th class="two wide">Branch</th>
                <th class="two wide">App Log</th>
                <th>Robot Parameter</th>
              </thead>
              <tbody>
                <tr v-for="map in tp.maps" :key="map.test" v-if="map.use">
                  <td>{{map.test}}</td>
                  <td>{{map.source_type}}</td>
                  <td>{{map.source_url}}</td>
                  <td>{{map.source_branch}}</td>
                  <td>{{map.app}}</td>
                  <td>{{map.robot_parameter}}</td>
                </tr>
              </tbody>
            </table>
          </td>
          <td class="center aligned">
              <button class="ui icon button blue" @click="runshow(tp)">
                <i class="play icon"></i>
                </button>
              <button class="ui icon button yellow" @click="url(tp)">
                <i class="paper plane icon"></i>
                </button>
          </td>
        </tr>
      </tbody>
    </table>
    <model  ref="runmodelcomponent" @yes="runproject" :name="run">
      <div slot="header">Run Project</div>
      <div slot="content">Are you sure run project?</div>
    </model>
    <model  ref="urlcomponent"  :name="URL">
      <div slot="header">URl</div>
      <div slot="content" v-html="urlresponse"></div>
    </model>
    <model  ref="jobmodelcomponent" @yes="tojob" :name="job" :noshow="false">
      <div slot="header">Status</div>
      <div slot="content" v-html="response"></div>
    </model>
  </div>
</template>
<script>
import model from '@/components/model'
import {labList} from '@/api/lab'
import {nodeList} from '@/api/node'
import {startjob} from '@/api/job'
export default {
  name: 'lab',
  components: {
    model
  },
  data () {
    return {
      active:"active",
      projects: [],
      run: 'run',
      job: 'job',
      URL: 'URL',
      project: this.$route.params.name,
      runitem: '',
      response: '',
      urlresponse: '',
      false: false,
      nodes: [{title: '', icon: ''}]
    }
  },
  watch: {
    '$route': ['fetchNodes', 'fetchData']
  },
  created () {
    this.fetchNodes()
    this.fetchData()
  },
  methods: {
    iconcss (node) {
      for (let n in this.nodes) {
        if (node === this.nodes[n].title) {
          return this.nodes[n].icon
        }
      }
    },
    toproject (item) {
      this.$router.push({name: 'toproject', params: {name: item}})
    },
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
      this.project = this.$route.params.name
      labList(this.params).then(response => {
        this.projects = response.data
        this.filterproject()
        this.active=""
      }).catch(()=>{
        this.active=""
      })
    },
    fetchNodes () {
      nodeList(null).then(response => {
        this.nodes = response.data
      })
    },
    runshow (tp) {
      this.runitem = tp.name
      this.$refs.runmodelcomponent.$emit('show')
    },
    url (tp) {
      this.urlresponse = 'curl http://baymax.ds.com:8080/api/job/' + tp.name + '/start'
      this.$refs.urlcomponent.$emit('show')
    },
    runproject () {
      this.response = '<i class="spinner loading icon"></i>'
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

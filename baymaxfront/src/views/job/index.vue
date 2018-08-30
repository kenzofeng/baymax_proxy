<template>
<div>
  <table class="ui compact selectable celled striped teal table">
    <thead>
      <tr>
        <th class="one wide">Project</th>
        <th class="one wide">Servers</th>
        <th class="one wide">Status</th>
        <th class="one wide">Start Date</th>
        <th class="one wide">End Date</th>
        <th>Test Automation</th>
        <th>Atction</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="job in jobs" :class="lineclass(job.status)" :key="job.pk">
        <td>{{job.project}}</td>
        <td>
            <div class="ui aligned divided list">
                <a class="item"  v-for="server in job.servers" :key="server">
                <i class="orange server icon"></i>
                <div class="content">
                    <div class="header">{{server}}</div>
                </div>
                </a>
            </div>
        </td>
        <td>
          <i class='icon' :class="statusclass(job.status)"></i>
          <span>{{job.status}}</span>
        </td>
        <td>{{job.start_time}}</td>
        <td>{{job.end_time}}</td>
        <td>
          <table class="ui small table very compact">
            <thead>
              <th class="two wide">Test</th>
              <th class="one wide">Version</th>
              <th>Robot Parameter</th>
              <th class="one wide">Status</th>
              <th class="two wide">RunTime Log</th>
              <th class="one wide">Report</th>
            </thead>
            <tbody>
              <tr v-for="test in job.job_test_set" :key="test.id">
                <td class="collapsing" >{{test.name}}</td>
                <td class="collapsing" >{{test.revision_number}}</td>
                <td class="collapsing" >{{test.robot_parameter}}</td>
                <td class="collapsing" :class="resultclass(test.status)" >{{test.status}}</td>
                <td class="collapsing">
                  <a target='_blank' :href="testlog(test.log)">
                    <i class='large file text outline icon'></i>
                  </a>
                </td>
                <td class="collapsing">
                  <a target='_blank' :href="testreport(test.id)">
                    <i class='large file text outline icon'></i>
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
        <td class="one wide">
            <div class="ui large buttons">
          <button class="ui icon button red" :class="buttonclass(job.status)" @click="stopshow(job.project)"><i class="stop icon"></i></button>
          <button class="ui icon button olive"  @click="rerunshow(job.pk,job.project)"><i class="undo icon"></i></button>
          <button class="ui icon button"><i class="paper plane icon"></i></button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
   <model  ref="stopmodelcomponent" @yes="stopproject" :name="stopm">
      <div slot="header">Stop Project:{{sproject}}</div>
      <div slot="content">Are you sure stop project?</div>
    </model>
    <model  ref="rerunmodelcomponent" @yes="rerunproject" :name="rerunm">
      <div slot="header">ReRun Project:{{rproject}}</div>
      <div slot="content">Are you sure rerun project?</div>
    </model>
    <model ref="notifymodelcomponent" :name="notify" :noshow='false'>
            <div slot="header">Status</div>
            <div slot="content">{{response}}</div>
    </model>
</div>
</template>
<script>
import {getall, stopjob, rerunjob} from '@/api/job'
import model from '@/components/model'
export default {
  name: 'job',
  components: {model},
  data () {
    return {
      jobs: null,
      params: this.$route.query,
      interval_id: '',
      stopm: 'stopm',
      rerunm: 'rerunm',
      notify: 'notifym',
      false: false,
      sproject: '',
      rproject: '',
      rjob: '',
      response: null
    }
  },
  created () {
    this.fetchData()
  },
  mounted () {
    this.Interval()
  },
  beforeDestroy () {
    clearInterval(this.interval_id)
  },
  methods: {
    Interval () {
      this.interval_id = setInterval(this.fetchData, 5000)
    },
    testlog (id) {
      return 'result/test/log/' + id
    },
    testreport (id) {
      return 'result/report/' + id
    },
    stopshow (item) {
      this.sproject = item
      this.$refs.stopmodelcomponent.$emit('show')
    },
    rerunshow (pk, project) {
      this.rproject = project
      this.rjob = pk
      this.$refs.rerunmodelcomponent.$emit('show')
    },
    stopproject () {
      stopjob(this.sproject).then(response => {
        this.response = response.data
      })
      this.$refs.notifymodelcomponent.$emit('show')
    },
    rerunproject () {
      rerunjob(this.rjob).then(response => {
        this.response = response.data
      })
      this.$refs.notifymodelcomponent.$emit('show')
    },
    fetchData () {
      getall(this.params).then(response => {
        this.jobs = response.data
      })
    },
    lineclass (i) {
      switch (i) {
        case 'Done':
          return 'positive'
        case 'Error':
          return 'error'
        case 'Running':case 'Waiting':
          return 'warning'
      }
    },
    statusclass (i) {
      switch (i) {
        case 'Done':
          return 'green checkmark'
        case 'Error':
          return 'red close'
        case 'Running':
          return 'spinner loading'
        case 'Waiting':
          return 'sync loading'
      }
    },
    resultclass (i) {
      switch (i) {
        case 'PASS':
          return 'positive'
        case 'Running':
          return 'warning'
        case 'FAIL': case 'Error':
          return 'error'
      }
    },
    buttonclass (i) {
      // if (i !== 'Running') {
      //   return 'disabled'
      // }
    }
  }
}
</script>

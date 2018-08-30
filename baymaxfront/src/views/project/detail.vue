<template>
    <div class="ui form">
        <h4 class="ui teal dividing header">Information</h4>
        <div class="two fields">
            <div class="required field">
                <label>Name:</label>
                <input type="text" name="name" v-model="item.name"></div>
            <div class="field">
                <label>Email:</label>
                <input type="text" name="email" placeholder="aaa@derbysoft.com;bbb@derbysoft.com" v-model="item.email"></div>
        </div>
        <h4 class="ui teal dividing header">Servers</h4>
        <div class="fields">
            <multidrop  :items="nodes" :value="item.nodes" @changeselected="changeselected" :isfluid="true"></multidrop>
        </div>
        <h4 class="ui teal header">Test Automation</h4>
        <div>
            <testauto  @dauto="deleteauto" :items="item.maps"></testauto>
        </div>
        <h4 class="ui teal dividing header"></h4>
        <div id="ttladd" class="ui blue small labeled icon button" @click="addauto">
            <i class="plus icon"></i>
            Add Automation
        </div>
        <h4 class="ui teal dividing header"></h4>
        <button class="ui green labeled icon button" @click="saveshow"><i class="save icon"></i>Save</button>
        <button class="ui teal labeled icon button" @click="gotolab"><i class="tasks icon"></i>Lab</button>
        <model ref="savemodelcomponent" @yes="saveproject" :name="savem">
            <div slot="header">Save Project</div>
            <div slot="content">Are you sure save project?</div>
        </model>
        <model ref="notifymodelcomponent" :name="notify" :noshow='false'>
            <div slot="header">Status</div>
            <div slot="content">{{response}}</div>
        </model>
    </div>
</template>
<script>
import {getdetail, saveproject} from '@/api/project'
import {getList} from '@/api/node'
import testauto from './testauto'
import multidrop from '@/components/multidropdown'
import model from '@/components/model'
export default {
  name: 'detail',
  data () {
    return {
      item: {},
      nodes: [],
      savem: 'save',
      notify: 'notify',
      response: null,
      false: false
    }
  },
  components: {testauto, multidrop, model},
  created () {
    this.fetchData()
    this.fetchNodes()
  },
  methods: {
    changeselected (nodes) {
      this.item.nodes = nodes
    },
    deleteauto (item) {
      this.item.maps.pop()
    },
    addauto () {
      this.item.maps.push({project: '', robot_parameter: '', test: '', testurl: '', use: true})
    },
    fetchData () {
      getdetail({tid: this.$route.params.name}).then(response => {
        this.item = response.data
      })
    },
    fetchNodes () {
      getList(null).then(response => {
        this.nodes = response.data
      })
    },
    saveshow () {
      this.$refs.savemodelcomponent.$emit('show')
    },
    saveproject () {
      saveproject(this.item).then(response => {
        this.response = response.data
      })
      this.$refs.notifymodelcomponent.$emit('show')
    },
    gotolab () {
      this.$router.push({name: 'labtoproject', params: {name: this.item.name}})
    }
  },
  watch: {
    $route: {
      handler: function (val, oldVal) {
        this.fetchData()
        this.fetchNodes()
      }
    }
  }
}
</script>

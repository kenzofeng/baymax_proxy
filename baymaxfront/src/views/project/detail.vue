<template>
    <div class="ui form">
        <div class="ui top attached inverted blue button" tabindex="0" >GoTo Test Lab</div>
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
            <multidrop  :items="nodes" :value="item.nodes"></multidrop>
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
        <div class="ui large buttons">
            <button class="ui red button">Delete</button>
            <div class="or"></div>
            <button class="ui teal button" @click="save">Save</button>
        </div>
    </div>
</template>
<script>
import {getdetail} from '@/api/project'
import {getList} from '@/api/node'
import testauto from './testauto'
import multidrop from '@/components/multidropdown'
export default {
  name: 'detail',
  data () {
    return {
      item: {},
      nodes: []
    }
  },
  components: {testauto, multidrop},
  created () {
    this.fetchData()
    this.fetchNodes()
  },
  methods: {
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
    save () {
      console.log(JSON.stringify(this.item))
    }
  },
  watch: {
    $route: {
      handler: function (val, oldVal) {
        this.fetchData()
      }
    }
  }
}
</script>

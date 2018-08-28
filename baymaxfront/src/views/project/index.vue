<template>
  <div class="ui internally celled grid">
    <div class="row">
      <div class="twelve wid column">
        <div class="ui action input">
          <multidrop :items="selectitems" @changeselected="changeselected"></multidrop>
          <button class="ui teal button" @click="show">
            <i class="clipboard list icon"></i>
            Project
          </button>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="three wide column">
        <list :items="items"></list>
      </div>
      <div class="thirteen wide column">
        <router-view></router-view>
      </div>
    </div>
    <actionmodel ref="actionmodelcomponent"  @yes="yes" ></actionmodel>
  </div>
</template>

<script>
import {
  getList
} from '@/api/project'
import multidrop from '@/components/multidropdown'
import actionmodel from '@/components/actionmodel'
import list from './list'
export default {
  name: 'project',
  data () {
    return {
      selectitems: {},
      items: {}
    }
  },
  components: {
    list, multidrop, actionmodel
  },
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      getList(null).then(response => {
        this.selectitems = response.data
        this.items = response.data
      })
    },
    changeselected (val) {
      if (val.length === 0) {
        this.items = this.selectitems
      } else {
        this.items = val
      }
    },
    show () {
      this.$refs.actionmodelcomponent.$emit('show')
    },
    yes (val) {
      console.log(val)
    }
  }
}

</script>

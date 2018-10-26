<template>
  <div class="ui internally celled grid">
    <div class="row">
      <div class="twelve wid column">
          <button class="ui teal button" @click="show">
            <i class="clipboard list icon"></i>
            Project
          </button>
      </div>
    </div>
    <div class="row">
      <div class="three wide column">
        <list :items="items" @deleteproject="deleteshow"></list>
      </div>
      <div class="thirteen wide column">
        <router-view></router-view>
      </div>
    </div>
    <actionmodel ref="actionmodelcomponent"  @yes="yes" ></actionmodel>
    <model ref="deletemodelcomponent" @yes="dproject" :name="deletem">
            <div slot="header">Delete Project</div>
            <div slot="content">Are you sure delete project?</div>
    </model>
    <model ref="notifymodelcomponent" :name="notify" :noshow="false">
            <div slot="header">Status</div>
            <div slot="content" v-html="response"></div>
        </model>
  </div>
</template>
<script>
import {getList, newproject, deleteproject} from '@/api/project'
import multidrop from '@/components/multidropdown'
import actionmodel from '@/components/actionmodel'
import model from '@/components/model'
import list from './list'
export default {
  name: 'project',
  data () {
    return {
      items: [],
      deletem: 'delete',
      notify: 'indexnotify',
      ditem: '',
      response: null,
      false: false
    }
  },
  components: {
    list, multidrop, actionmodel, model
  },
  created () {
    this.fetchData()
  },
  methods: {
    dproject () {
      this.response = '<i class="spinner loading icon"></i>'
      deleteproject(this.ditem).then(response => {
        this.response = response.data
        this.fetchData()
      })
      this.$refs.notifymodelcomponent.$emit('show')
    },
    deleteshow (item) {
      this.ditem = item
      this.$refs.deletemodelcomponent.$emit('show')
    },
    fetchData () {
      getList(null).then(response => {
        this.items = response.data
      })
    },
    show () {
      this.$refs.actionmodelcomponent.$emit('show')
    },
    yes (val) {
      newproject(val).then(response => {
        this.fetchData()
      })
    }
  }
}

</script>

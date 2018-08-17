<template>
    <div class="ui internally celled grid">
        <div class="row">
            <div class="twelve wid column">
                <div class="ui tiny teal button"><i class="plus icon"></i>
                    project
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
    </div>
</template>

<script>
import {getList} from '@/api/project'
import list from './list'
export default {
  name: 'project',
  data () {
    return {
      items: {}
    }
  },
  components: {list},
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      getList(null).then(response => {
        this.items = response.data
      })
    }
  }
}
</script>

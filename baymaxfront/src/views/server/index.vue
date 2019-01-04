<template>
  <div class="dimmable">
    <div class="ui inverted dimmer" :class="active">
      <div class="ui loader"></div>
    </div>
    <table class="ui selectable celled teal table">
      <thead>
        <tr>
          <th>Name</th>
          <th>ID</th>
          <th>IP</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="server in servers" :key="server.id">
          <td class="ui aligned header" :class="statuscss(server.icon)">{{server.title}}</td>
          <td>{{server.id}}</td>
          <td>{{server.ip}}</td>
          <td><i class="circle icon" :class="statuscss(server.icon)"></i></td>
        </tr>
    </tbody>
    </table>
  </div>
</template>
<script>
import {nodeList} from '@/api/node'
export default {
  name: 'server',
  data () {
    return {
      active:"active",
      servers: []
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      nodeList(this.params).then(response => {
        this.servers = response.data
        this.active=""
      }).catch(()=>{
        this.active=""
      })
    },
    statuscss (icon) {
      return icon
    }
  }
}

</script>

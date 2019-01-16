<template>
  <div class="dimmable">
    <div class="ui inverted dimmer" :class="active">
      <div class="ui loader"></div>
    </div>
    <table class="ui compact selectable definition celled padded table">
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>ID</th>
          <th>IP</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(server,index) in servers" :key="server.id" :class="statuscss(server.icon)">
          <td>{{index+1}}</td>
          <td :class="statuscss(server.icon)">{{server.title}}</td>
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
  watch: {
    $route: ["fetchData"]
  },
  methods: {
    fetchData () {
      this.params = this.$route.query;
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

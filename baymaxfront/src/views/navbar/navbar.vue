<template>
  <div class="ui teal inverted huge menu">
    <div class="header item">
      Baymax System
    </div>
    <navitem v-for="router in routes" :key=" router.name" :item="router"></navitem>
    <div class="right menu">
    <a class="item" target='_blank' href="https://devops.dbaws.net/aws/home/sandbox_warrior/us-west-2/Function/"><i class="cloud icon"></i>AWS</a>
    <a class="item" target='_blank' href="http://54.218.22.41/"><i class="wrench icon"></i>TestRailTool</a>
    <a class="item" target='_blank' href="https://warrior.testrail.io/index.php?/dashboard"><i class="industry icon"></i>TestRail</a>
  </div>
  </div>
</template>

<script>
import navitem from './navitem'
export default {
  name: 'navbar',
  components: {navitem},
  computed: {
    routes () {
      return this.$router.options.routes
    }
  }
}
</script>

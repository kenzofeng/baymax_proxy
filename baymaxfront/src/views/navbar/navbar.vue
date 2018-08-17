<template>
  <div class="ui teal three item inverted huge menu">
    <navitem v-for="router in routes" :key=" router.name" :item="router"></navitem>
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

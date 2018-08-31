<template>
    <router-link :class="{active : isActive()}" class="item" v-if="item.menu" :to="item.path"><i :class="item.icon" class="icon"></i>{{item.name}}</router-link>
</template>

<script>
export default {
  name: 'navitem',
  props: {
    item: {}
  },
  methods: {
    isActive () {
      if (this.$route.path.includes(this.item.name.toLowerCase())) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

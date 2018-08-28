<template>
    <router-link :class="Active()" class="item" :to="'/project/index/'+item">
                <i class="clipboard list icon"></i>
                <div class="content">
                    <div class="header">{{item}}</div>
                </div>
            </router-link>
</template>

<script>
export default {
  name: 'item',
  props: {
    item: {}
  },
  methods: {
    Active () {
      if (this.$route.params.name === this.item) {
        return {active: true}
      } else {
        return {active: false}
      }
    }
  }
}
</script>

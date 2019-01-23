<template>
        <div class="ui divided aligned selection list">
            <item v-for="item in items" :key="item.title" :item="item.title" @deleteproject="deleteproject"> </item>
        </div>
</template>

<script>
import item from './item'

export default {
  name: 'list',
  components: {item},
  props: {
    items: {}
  },
  methods: {
    deleteproject (item) {
      this.$emit('deleteproject', item)
    }
  }
}
</script>
<style >

</style>

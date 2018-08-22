<template>
    <select  multiple=""   class="ui fluid search dropdown" :value="value" v-model="selected">
        <option value="">Servers</option>
        <option v-for="item in items" :value="item" :key="item">{{item}}</option>
    </select >
</template>
<script>
export default {
  name: 'multidrop',
  data () {
    return {
      selected: []
    }
  },
  props: {items: null, value: null},
  mounted () {
    $('.dropdown').dropdown()
  },
  watch: {
    value (val) {
      $('.dropdown').dropdown('clear')
      for (var s in val) {
        $('.dropdown').dropdown('set selected', val[s])
      }
      this.selected = val
    },
    selected (val) {
      this.$emit('changeselected', val)
    }
  }
}
</script>

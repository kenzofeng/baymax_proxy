<template>
    <select  multiple="" :class="{fluid:isfluid}"  class="ui search dropdown" :value="value" v-model="selected">
        <option value=""></option>
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
  props: {items: null, value: null, isfluid: false},
  mounted () {
    $('.dropdown').dropdown()
  },
  watch: {
    value (val) {
      $('.dropdown').dropdown('clear')
      val.forEach(function (val) {
        $('.dropdown').dropdown('set selected', val)
      })
      this.selected = val
    },
    selected (val) {
      this.$emit('changeselected', val)
    }
  }
}
</script>

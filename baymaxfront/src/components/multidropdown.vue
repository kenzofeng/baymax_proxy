<template>
    <select  multiple="" :class="{fluid:isfluid}"  class="ui search dropdown" v-model="selected">
        <option value=""></option>
        <option v-for="item in items" :value="item.title" :key="item.title"><i :class="iconcss(item)"></i>{{item.title}}</option>
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
  props: {items: null, default: null, isfluid: false},
  mounted () {
    $(this.$el).dropdown()
  },
  watch: {
    default: {
      handler (newval, oldval) {
        let _dropdwon = this
        $(_dropdwon.$el).dropdown('clear')
        if (newval !== undefined) {
          newval.forEach(function (val) {
            $(_dropdwon.$el).dropdown('set selected', val)
          })
          _dropdwon.selected = newval
        }
      }
    },
    selected (val) {
      this.$emit('changeselected', val)
    }
  },
  methods: {
    iconcss (item) {
      return item.icon + ' server icon'
    }
  }
}
</script>

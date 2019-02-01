<template>
    <select class="ui search dropdown" v-model="selected">
        <option value=""></option>
        <option v-for="item in items" :value="item.title" :key="item.title"><i :class="iconcss(item)"></i>{{item.title}}</option>
    </select >
</template>
<script>
export default {
  name: 'drop',
  data () {
    return {
      selected: []
    }
  },
  props: {items: null, default: null},
  mounted () {
    $(this.$el).dropdown({
      clearable: true,
      placeholder:""
    })
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
      return item.icon
    }
  }
}
</script>

<template>
    <div class="ui modal" :class="name" >
    <i class="close icon"></i>
    <div class="header">
        <slot name="header"></slot>
    </div>
    <div class="content">
         <slot name="content"></slot>
    </div>
    <div class="actions">
        <div class="ui red deny button">No</div>
        <div class="ui green approve button">Yes</div>
    </div>
</div>
</template>
<script>
export default {
  name: 'model',
  props: {
    name: null
  },
  mounted () {
    let _model = this
    this.$on('show', () => {
      $('.ui.modal.' + this.name).modal({
        observeChanges: true,
        onApprove () {
          _model.$emit('yes', 'yes')
        }
      }).modal('show')
    })
  },
  beforeDestroy () {
    $('.ui.modals').remove()
  }
}
</script>

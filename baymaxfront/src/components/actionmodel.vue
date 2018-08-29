<template>
  <div class="ui large modal action">
    <i class="close icon"></i>
    <div class="header">New Project</div>
    <div class="content">
      <div class="ui form" >
        <h4 class="ui teal dividing header">Project Name</h4>
        <div class="tow fields">
          <div class="required eight wide field">
            <label>Name:</label>
            <input type="text" v-model="name">
          </div>
        </div>
      </div>
    </div>
    <div class="actions">
      <div class="ui red deny button">Cancel</div>
      <div class="ui green approve button">Save</div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'actionmodel',
  data () {
    return {
      name: ''
    }
  },
  mounted () {
    let _model = this
    this.$on('show', () => {
      $('.ui.modal.action').modal({
        observeChanges: true,
        onApprove () {
          _model.$emit('yes', _model.name)
        }
      }).modal('show')
    })
  },
  beforeDestroy () {
    $('.ui.modals').remove()
  }
}

</script>

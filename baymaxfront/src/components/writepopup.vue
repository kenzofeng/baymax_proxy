<template>
  <div class="ui large modal comments">
    <div class="header">Comments</div>
    <div class="content">
      <div class="ui form">
          <div class="field">
               <textarea v-model="comment"></textarea>
          </div>
      </div>
    </div>
    <div class="actions">
      <div class="ui red deny button">Cancel</div>
      <div class="ui green approve button">OK</div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'writepopup',
  data () {
    return {
      comment: {},
      index: ''
    }
  },
  mounted () {
    this.setupmodal()
  },
  methods: {
    setupmodal () {
      let _modal = this
      $(this.$el).modal({
        observeChanges: true,
        duration: 0,
        dimmerSettings: {
          opacity: 0
        },
        onApprove () {
          _modal.$emit('savecomments', _modal.comment, _modal.index)
        }
      })
    },
    show (val, index) {
      this.index = index
      this.comment = val
      $(this.$el).modal('show')
    }
  },
  beforeDestroy () {
    $('.ui.modals').remove()
  }
}

</script>

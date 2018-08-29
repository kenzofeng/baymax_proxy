<template>
 <div :class="Active()" class="item" @click="tonext(item)">
    <div class="right floated content">
      <i class="red trash alternate outline icon" @click="deleteproject(item)"></i>
    </div>
    <i class="clipboard list icon"></i>
      <div class="content">
        <div class="header">{{item}}</div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'item',
  props: {
    item: {}
  },
  methods: {
    deleteproject (item) {
      this.$emit('deleteproject', item)
    },
    tonext () {
      this.$router.push({
        name: 'toproject',
        params: {
          name: this.item
        }
      })
    },
    Active () {
      if (this.$route.params.name === this.item) {
        return {
          active: true
        }
      } else {
        return {
          active: false
        }
      }
    }
  }
}

</script>

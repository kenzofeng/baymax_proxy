<template>
    <div>
        <div v-for="item in items" :key="item.pk">
            <h4 class="ui teal dividing header"></h4>
            <div class="fields">
                <div class="required five wide field">
                    <label>Test Name:</label>
                    <input type="text" v-model="item.test"></div>
                <div class="required ten wide field">
                    <label>Automation URL:</label>
                    <input type="text" v-model="item.testurl"></div>
            </div>
            <div class="fields">
                <div class="five wide field">
                    <label >Robot Parameters:</label>
                    <input type="text" v-model="item.robot_parameter"></div>
                <div class="five wide field">
                    <label>App Log:</label>
                    <input type="text" v-model="item.app"></div>
                <div class="field">
                    <label>Enable</label>
                    <div class="ui toggle checkbox">
                        <input type="checkbox" v-model="item.use">
                        <label></label>
                    </div>
                </div>
            </div>
            <button class="ui red button" @click="deleteauto(item)">Delete</button>
        </div>
    </div>
</template>
<script>
export default {
  name: 'testauto',
  props: {
    items: null
  },
  methods: {
    deleteauto (item) {
      this.$emit('dauto', item)
    }
  }
}
</script>

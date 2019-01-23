<template>
  <div>
    <div v-for="item in items" :key="item.pk">
      <h4 class="ui teal dividing header"></h4>
      <div class="fields">
        <div class="required fifteen wide field">
          <label>Test Name:</label>
          <input type="text" v-model="item.test">
        </div>
      </div>
      <div class="fields">
        <div class="required three wide field">
          <label>Type:</label>
          <select class="ui dropdown" v-model="item.source_type">
            <option value>Type</option>
            <option value="Git">Git</option>
            <option value="SVN">SVN</option>
          </select>
        </div>
        <div class="eight wide field">
          <label>URL:</label>
          <input type="text" v-model="item.source_url">
        </div>
        <div class="four wide field">
          <label>Branch:</label>
          <input type="text" v-model="item.source_branch">
        </div>
      </div>
      <div class="fields">
        <div class="five wide field">
          <label>App Log:</label>
          <input type="text" v-model="item.app">
        </div>
        <div class="ten wide field">
          <label>Robot Parameters:</label>
          <input type="text" v-model="item.robot_parameter">
        </div>
        <div class="one wide field">
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
  name: "testauto",
  props: {
    items: null
  },
  watch: {
    items(n, o){
      this.$nextTick(() => {
        $('.ui.dropdown').dropdown()
      });
    }
  },
  methods: {
    deleteauto(item) {
      this.$emit("dauto", item);
    }
  }
};
</script>

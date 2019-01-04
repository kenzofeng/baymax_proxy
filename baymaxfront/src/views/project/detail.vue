<template>
  <div class="dimmable">
    <div class="ui inverted dimmer" :class="active">
      <div class="ui loader"></div>
    </div>
    <div class="ui form">
      <h4 class="ui teal dividing header">Information</h4>
      <div class="two fields">
        <div class="required field">
          <label>Name:</label>
          <input type="text" name="name" v-model="item.name">
        </div>
        <div class="required field">
          <label>Email:</label>
          <input
            type="text"
            name="email"
            placeholder="aaa@derbysoft.com;bbb@derbysoft.com"
            v-model="item.email"
          >
        </div>
      </div>
      <div class="field">
        <label>Version:</label>
        <input
          type="text"
          name="version"
          placeholder="/project1/git.properties;/project2/git.properties"
          v-model="item.version"
        >
      </div>
      <h4 class="ui teal dividing header">Servers</h4>
      <div class="fields">
        <multidrop
          :items="nodes"
          :default="item.nodes"
          @changeselected="changeselected"
          :isfluid="true"
        ></multidrop>
      </div>
      <h4 class="ui teal header">Test Automation</h4>
      <div>
        <testauto @dauto="deleteauto" :items="item.maps"></testauto>
      </div>
      <h4 class="ui teal dividing header"></h4>
      <div id="ttladd" class="ui blue small labeled icon button" @click="addauto">
        <i class="plus icon"></i>
        Add Automation
      </div>
      <h4 class="ui teal dividing header"></h4>
      <button class="ui green labeled icon button" @click="saveshow">
        <i class="save icon"></i>Save
      </button>
      <button class="ui teal labeled icon button" @click="gotolab">
        <i class="flask icon"></i>Lab
      </button>
      <model ref="savemodelcomponent" @yes="saveproject" :name="savem">
        <div slot="header">Save Project</div>
        <div slot="content">Are you sure save project?</div>
      </model>
      <model ref="notifymodelcomponent" :name="notify" :noshow="false">
        <div slot="header">Status</div>
        <div slot="content" v-html="response"></div>
      </model>
    </div>
  </div>
</template>
<script>
import { getdetail, saveproject } from "@/api/project";
import { nodeList } from "@/api/node";
import testauto from "./testauto";
import multidrop from "@/components/multidropdown";
import model from "@/components/model";
export default {
  name: "detail",
  data() {
    return {
      active:"active",
      item: { name: "", email: "", version: "", nodes: [], maps: [] },
      nodes: [],
      savem: "save",
      notify: "notify",
      response: null,
      false: false
    };
  },
  components: { testauto, multidrop, model },
  created() {
    this.fetchNodes();
    this.fetchData();
  },
  methods: {
    changeselected(nodes) {
      this.item.nodes = nodes;
    },
    deleteauto(item) {
      this.item.maps.pop();
    },
    addauto() {
      this.item.maps.push({
        project: "",
        robot_parameter: "",
        test: "",
        source_type: "Git",
        source_url: "",
        source_branch: "master",
        app: "",
        use: true
      });
    },
    fetchData() {
      this.active="active"
      getdetail({ tid: this.$route.params.name })
        .then(response => {
          this.item = response.data;
          this.active = "";
        })
        .catch(() => {
          this.active = "";
        });
    },
    fetchNodes() {
      nodeList(null).then(response => {
        this.nodes = response.data;
      });
    },
    saveshow() {
      this.$refs.savemodelcomponent.$emit("show");
    },
    saveproject() {
      this.response = '<i class="spinner loading icon"></i>';
      saveproject(this.item).then(response => {
        this.response = response.data;
      });
      this.$refs.notifymodelcomponent.$emit("show");
    },
    gotolab() {
      this.$router.push({
        name: "labtoproject",
        params: { name: this.item.name }
      });
    }
  },
  watch: {
    $route: {
      handler: function(val, oldVal) {
        this.fetchData();
        this.fetchNodes();
      }
    }
  }
};
</script>

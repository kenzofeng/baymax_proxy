<template>
  <div>
    <div class="ui form">
      <div class="fields">
        <div class="field">
          <div class="ui checkbox">
            <input v-model="version" type="checkbox" name="Version">
            <label>Version</label>
          </div>
          <div class="ui checkbox">
            <input v-model="servers" type="checkbox" name="Servers">
            <label>Servers</label>
          </div>
        </div>
      </div>
    </div>
    <table class="ui selectable celled striped teal table">
      <thead>
        <tr>
          <th class="one wide">Project</th>
          <th v-if="version" class="one wide">Version</th>
          <th v-if="servers" class="one wide">Servers</th>
          <th class="one wide">Status</th>
          <th class="one wide">Start Date</th>
          <th class="one wide">End Date</th>
          <th class="seven wide">Test Automation</th>
          <!-- <th class="one wide">Comments</th> -->
          <th class="one wide">Atction</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in jobs" :class="lineclass(job.status)" :key="job.pk">
          <td>{{job.project}}</td>
          <td v-if="version">{{job.project_version}}</td>
          <td v-if="servers">
            <div v-for="s in jobServers(job.servers)" :key="s">{{s}}</div>
          </td>
          <td>
            <i class="icon" :class="statusclass(job.status)"></i>
            <span>{{job.status}}</span>
          </td>
          <td>{{job.start_time}}</td>
          <td>{{job.end_time}}</td>
          <td>
            <table class="ui small very compact table">
              <thead>
                <th class="two wide">Test</th>
                <th class="one wide">Version</th>
                <th class="four wide">App Log</th>
                <th class="six wide">Robot Parameter</th>
                <th class="one wide">Status</th>
                <th class="one wide">RunTime</th>
                <th class="one wide">Report</th>
              </thead>
              <tbody>
                <tr v-for="test in job.job_test_set" :key="test.id">
                  <td>{{test.name}}</td>
                  <td>
                    <span
                      class="ui span"
                      :data-tooltip="test.revision_number"
                      data-position="right center"
                    >{{showdata(test.revision_number)}}</span>
                  </td>
                  <td>{{test.app}}</td>
                  <td>{{test.robot_parameter}}</td>
                  <td :class="resultclass(test.status)">{{test.status}}</td>
                  <td>
                    <a target="_blank" :href="testlog(test.log)">
                      <i class="large file text outline icon"></i>
                    </a>
                  </td>
                  <td>
                    <a target="_blank" :href="testreport(test.id)">
                      <i class="large file text outline icon"></i>
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
          <!-- <td class="collapsing" @dblclick="editcomments(job.comments,job.pk)">
            <span
              class="ui span"
              :data-tooltip="job.comments"
              data-position="top right"
            >{{showdata(job.comments)}}</span>
          </td>-->
          <td>
            <div class="ui icon buttons">
              <button
                class="ui icon button red"
                :class="buttonclass(job.status)"
                @click="stopshow(job.project)"
              >
                <i class="stop icon"></i>
              </button>
              <button class="ui icon button olive" @click="rerunshow(job)">
                <i class="undo icon"></i>
              </button>
              <a class="ui icon button" target="_blank" :href="downloadxml(job.pk)">
                <i class="download icon"></i>
              </a>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <model ref="stopmodelcomponent" @yes="stopproject" :name="stopm">
      <div slot="header">Stop Project:{{sproject}}</div>
      <div slot="content">Are you sure stop project?</div>
    </model>
    <model ref="rerunmodelcomponent" @yes="rerunproject" :name="rerunm">
      <div slot="header">ReRun Project:{{rproject}}</div>
      <div slot="content">
        <div class="ui form">
          <table class="ui small very compact table">
            <thead>
              <th class="two wide">Test</th>
              <th class="six wide">Robot Parameter</th>
            </thead>
            <tbody>
              <tr v-for="test in form.job.job_test_set" :key="test.id">
                <td>{{test.name}}</td>
                <td>
                  <input type="text" v-model="test.robot_parameter">
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </model>
    <model ref="notifymodelcomponent" :name="notify" :noshow="false">
      <div slot="header">Status</div>
      <div slot="content" v-html="response"></div>
    </model>
    <writepopup ref="writepopup" @savecomments="savecomments"></writepopup>
  </div>
</template>
<script>
import { getall, stopjob, rerunjob, savecomment } from "@/api/job";
import model from "@/components/model";
import writepopup from "@/components/writepopup";
export default {
  name: "job",
  components: {
    model,
    writepopup
  },
  data() {
    return {
      jobs: null,
      params: this.$route.query,
      interval_id: "",
      stopm: "stopm",
      rerunm: "rerunm",
      notify: "notifym",
      false: false,
      sproject: "",
      rproject: "",
      rjob: "",
      response: null,
      form: { job: { job_test_set: [] } },
      activejob: {},
      version: false,
      servers: false
    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    $route: ["fetchData"]
  },
  mounted() {
    this.Interval();
  },
  beforeDestroy() {
    clearInterval(this.interval_id);
  },
  methods: {
    jobServers(data) {
      let servers = data.split(":");
      return servers;
    },
    showdata(data) {
      if (data != null) {
        if (data.length > 12) {
          return data.slice(0, 12) + "...";
        }
      }
      return data;
    },
    editcomments(comments, pk) {
      this.$refs.writepopup.show(comments, pk);
    },
    savecomments(comments, pk) {
      savecomment({ id: pk, comments: comments });
      for (let job of this.jobs) {
        if (job.pk === pk) {
          job.comments = comments;
        }
      }
    },
    onCopy(e) {
      alert("You just copied: " + e.text);
    },
    toproject(item) {
      this.$router.push({
        name: "toproject",
        params: {
          name: item
        }
      });
    },
    Interval() {
      this.interval_id = setInterval(this.fetchData, 5000);
    },
    testlog(id) {
      return "result/test/log/" + id;
    },
    testreport(id) {
      return "result/report/" + id;
    },
    downloadxml(id) {
      return "result/report/" + id + "/download";
    },
    stopshow(item) {
      this.sproject = item;
      this.$refs.stopmodelcomponent.$emit("show");
    },
    rerunshow(job) {
      this.rproject = job.project;
      this.rjob = job.pk;
      this.form.job = job;
      this.$refs.rerunmodelcomponent.$emit("show");
    },
    stopproject() {
      this.response = '<i class="spinner loading icon"></i>';
      stopjob(this.sproject).then(response => {
        this.response = response.data;
      });
      this.$refs.notifymodelcomponent.$emit("show");
    },
    rerunproject() {
      this.response = '<i class="spinner loading icon"></i>';
      rerunjob(this.rjob, this.form.job).then(response => {
        this.response = response.data;
      });
      this.$refs.notifymodelcomponent.$emit("show");
    },
    fetchData() {
      this.params = this.$route.query;
      getall(this.params).then(response => {
        this.jobs = response.data;
      });
    },
    lineclass(i) {
      switch (i) {
        case "Done":
          return "positive";
        case "Error":
          return "error";
        case "Running":
        case "Waiting":
          return "warning";
      }
    },
    statusclass(i) {
      switch (i) {
        case "Done":
          return "green checkmark";
        case "Error":
          return "red close";
        case "Running":
          return "spinner loading";
        case "Waiting":
          return "sync loading";
      }
    },
    resultclass(i) {
      switch (i) {
        case "PASS":
          return "positive";
        case "Running":
          return "warning";
        case "FAIL":
        case "Error":
          return "error";
      }
    },
    buttonclass(i) {
      if (i !== "Running") {
        return "disabled";
      }
    }
  }
};
</script>
<template>
  <div class="dimmable">
    <div class="ui inverted dimmer" :class="active">
      <div class="ui loader"></div>
    </div>
    <div class="ui grid">
      <div class="two wide column">
        <h5 class="ui header"></h5>
        <div class="ui checkbox">
          <input v-model="projectid" type="checkbox" name="ID">
          <label>ID</label>
        </div>
        <div class="ui checkbox">
          <input v-model="version" type="checkbox" name="Version">
          <label>Version</label>
        </div>
        <div class="ui checkbox">
          <input v-model="servers" type="checkbox" name="Servers">
          <label>Servers</label>
        </div>
      </div>
      <div class="four wide column">
        <div class="ui fluid action input">
          <input type="text" placeholder="Project Version" v-model="project_version">
          <button class="ui icon button" @click="search_version">
            <i class="search icon"></i>
          </button>
        </div>
      </div>
    </div>
    <table class="ui selectable celled striped teal table">
      <thead>
        <tr>
          <th v-if="projectid" class="one wide">ID</th>
          <th class="one wide">Project</th>
          <th v-if="version" class="one wide">Version</th>
          <th v-if="servers" class="one wide">Servers</th>
          <th class="one wide">Status</th>
          <th class="one wide">Start Date</th>
          <!-- <th class="one wide">End Date</th> -->
          <th class="six wide">Test Automation</th>
          <!-- <th class="one wide">Comments</th> -->
          <th class="one wide">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in jobs" :class="lineclass(job.status)" :key="job.pk">
          <td v-if="projectid">{{job.pk}}</td>
          <td>
            <a target="_blank" :href="project_log(job.pk)">
              <i class="linkify icon"></i>
            </a>
            {{job.project}}
          </td>
          <td v-if="version">{{job.project_version}}</td>
          <td v-if="servers">
            <div class="ui aligned ordered divided list">
              <div class="item" v-for="s in jobServers(job.servers)" :key="s">
                <div class="content">
                  <div class="header">{{s}}</div>
                </div>
              </div>
            </div>
          </td>
          <td>
            <i class="icon" :class="statusclass(job.status)"></i>
            <span>{{job.status}}</span>
          </td>
          <td>{{job.start_time}}</td>
          <!-- <td>{{job.end_time}}</td> -->
          <td>
            <table class="ui small very compact table">
              <thead>
                <th class="two wide">Test</th>
                <th class="one wide">Version</th>
                <th class="one wide">Duration</th>
                <th class="four wide">App Log</th>
                <th class="six wide">Robot Parameter</th>
                <th class="one wide">Count</th>
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
                  <td>{{test.duration}}</td>
                  <td>{{test.app}}</td>
                  <td>{{test.robot_parameter}}</td>
                  <td>{{test.count}}</td>
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
                @click="stopshow(job)"
              >
                <i class="stop icon"></i>
              </button>
              <button class="ui icon button olive" @click="rerunshow(job)">
                <i class="undo icon"></i>
              </button>
              <a class="ui icon button" target="_blank" :href="downloadxml(job.pk)">
                <i class="download icon"></i>
              </a>
              <button
                class="ui icon button red"
                :class="remove_buttonclass(job.status)"
                @click="removeshow(job)"
              >
                <i class="trash alternate icon"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <model ref="stopmodelcomponent" @yes="stopproject" :name="stopm">
      <div slot="header">Stop Project:{{sproject.project}}</div>
      <div slot="content">Are you sure stop project?</div>
    </model>
    <model ref="removemodelcomponent" @yes="removeproject" :name="revmovem">
      <div slot="header">Remove Project:{{rmproject}}</div>
      <div slot="content">Are you sure remove project?</div>
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
import { getall, stopjob, rerunjob, savecomment, rmjob } from "@/api/job";
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
      active: "active",
      jobs: null,
      params: this.$route.query,
      interval_id: "",
      stopm: "stopm",
      revmovem: "revmovem",
      rerunm: "rerunm",
      notify: "notifym",
      false: false,
      sproject: "",
      rproject: "",
      rmproject: "",
      rmjob: "",
      rjob: "",
      response: null,
      form: { job: { job_test_set: [] } },
      activejob: {},
      version: false,
      servers: false,
      projectid: false,
      project_version: ""
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
    search_version() {
      this.$router.push({
        path: "/job/index",
        query: { number: 30, version: this.project_version }
      });
    },
    jobServers(data) {
      let servers = data.split(":");
      return servers;
    },
    showdata(data) {
      if (data != null) {
        if (data.length > 8) {
          return data.slice(0, 8) + "...";
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
    project_log(id) {
      return "/job/index?id=" + id;
    },
    testlog(id) {
      return "/result/test/log/" + id;
    },
    testreport(id) {
      return "/result/report/" + id;
    },
    downloadxml(id) {
      return "/result/report/" + id + "/download";
    },
    stopshow(item) {
      console.log(item)
      this.sproject = item;
      this.$refs.stopmodelcomponent.$emit("show");
    },
    removeshow(job) {
      this.rmproject = job.project;
      this.rmjob = job.pk;
      this.$refs.removemodelcomponent.$emit("show");
    },
    rerunshow(job) {
      this.rproject = job.project;
      this.rjob = job.pk;
      this.form.job = job;
      this.$refs.rerunmodelcomponent.$emit("show");
    },
    stopproject() {
      this.response = '<i class="spinner loading icon"></i>';
      stopjob(this.sproject.project,this.sproject.pk).then(response => {
        this.response = response.data;
      });
      this.$refs.notifymodelcomponent.$emit("show");
    },
    removeproject() {
      this.response = '<i class="spinner loading icon"></i>';
      rmjob(this.rmjob).then(response => {
        this.response = response.data;
      });
      this.$refs.notifymodelcomponent.$emit("show");
      this.fetchData();
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
      getall(this.params)
        .then(response => {
          this.jobs = response.data;
          this.active = "";
        })
        .catch(() => {
          this.active = "";
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
        case "Waiting Job":
          return "sync loading";
        case "Waiting Server":
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
    },
    remove_buttonclass(i) {
      if (i == "Running" || i=="Waiting") {
        return "disabled";
      }
    }
  }
};
</script>

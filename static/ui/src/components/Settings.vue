<template>
  <v-container>
    <v-row class="text-center">
      <span class="text-h2 col-12 text-center font-weight-lighter"
        >Settings</span
      >
      <v-col cols="6">
        <blockquote class="blockquote ma6 text-left">
          <br />
          Setup your tasmotas against the configured mqtt URI, they will shortly
          start appearing below.<br /><br />
          <v-text-field
            hide-details
            dense
            label="MQTT IP"
            v-model="saveSettings.url"
          ></v-text-field>
        </blockquote>
      </v-col>
      <v-col cols="6">
        <blockquote class="blockquote ma6 text-left">
          <br />
          There, you'll have the chance to configure wich pump controls each
          alcohol and how many cl per second will it out.
        </blockquote>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="4"
        v-bind:key="title"
        v-for="(tasmota, title) in settings.tasmotas"
      >
        <v-card class="mx-auto" max-width="400">
          <v-card-title>
            <v-icon large left> mdi-gas-station-outline </v-icon>
            <span class="text-h6 font-weight-light">{{ title }}</span>
          </v-card-title>

          <v-card-text class="text-h5 font-weight-bold">
            <v-row v-bind:key="position" v-for="(relay, position) in tasmota">
              <v-col pa0 ma0>
                <v-checkbox
                  dense
                  hide-details
                  v-model="saveSettings.tasmotas[title][position][2]"
                  :label="`Relay ${position}`"
                ></v-checkbox
                >&nbsp;&nbsp;
              </v-col>
              <v-col pa0 ma0>
                <v-select
                  hide-details
                  :items="ingredients"
                  v-model="saveSettings.tasmotas[title][position][0]"
                  dense
                  label="Alcohol"
                ></v-select
              ></v-col>
              <v-col pa0 ma0>
                <v-text-field
                  hide-details
                  dense
                  v-model="saveSettings.tasmotas[title][position][1]"
                  class="mt-1 pt-0"
                  type="number"
                  style="width: 60px"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn block color="primary" @click="save()" elevation="7" large
          >Save settings</v-btn
        >
      </v-col>
      <v-col>
        <v-btn
          block
          color="secondary"
          @click="updateTasmotas()"
          elevation="7"
          large
          >Find new tasmotas</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Settings",
  data: function () {
    return { saveSettings: [], ingredients: [], settings: [] };
  },
  methods: {
    async save() {
      await window.axios.post("/settings", this.saveSettings);
      this.$emit('saved')
    },
    async updateTasmotas() {
      this.settings = await window.axios.get(`/settings`);
      this.saveSettings = this.settings;
    },
  },
  async mounted() {
    this.settings = await window.axios.get(`/settings`);
    this.saveSettings = this.settings;
    this.ingredients = await window.axios.get(`/alcohols`);
  },
};
</script>

<style scoped></style>

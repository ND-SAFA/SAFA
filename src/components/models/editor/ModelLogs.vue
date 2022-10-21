<template>
  <v-container>
    <v-timeline dense>
      <v-timeline-item color="primary lighten-3" small>
        <v-row class="pt-1">
          <v-col cols="3">
            <typography bold value="Pre-Training" />
          </v-col>
          <v-col>
            <typography value="Collected Keywords" />
            <div>
              <v-chip outlined class="ma-1">Automotive</v-chip>
            </div>
          </v-col>
        </v-row>
      </v-timeline-item>
      <v-timeline-item color="primary lighten-3" small>
        <v-row class="pt-1">
          <v-col cols="3">
            <typography bold value="Pre-Training" />
          </v-col>
          <v-col>
            <typography value="Trained On Documents" />
            <div>
              <v-chip outlined class="ma-1">SomeAutomotiveManual.pdf</v-chip>
            </div>
          </v-col>
        </v-row>
      </v-timeline-item>
      <v-timeline-item color="primary lighten-3" small>
        <v-row class="pt-1">
          <v-col cols="3">
            <typography bold value="Pre-Training" />
          </v-col>
          <v-col>
            <typography value="Trained On Repositories" />
            <div>
              <v-chip outlined class="ma-1">ND-SAFA/fend</v-chip>
            </div>
          </v-col>
        </v-row>
      </v-timeline-item>
      <v-timeline-item color="primary" small>
        <v-row class="pt-1">
          <v-col cols="3">
            <typography bold value="Training" />
          </v-col>
          <v-col>
            <typography value="Trained On Project" />
            <div>
              <v-chip color="primary" class="ma-1">My Project</v-chip>
              <v-chip outlined>Designs To Requirements</v-chip>
            </div>
          </v-col>
          <v-col cols="2">
            <v-btn outlined color="error">Revert</v-btn>
          </v-col>
        </v-row>
      </v-timeline-item>
    </v-timeline>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography } from "@/components/common";

/**
 * Displays logs of the model's training process.
 */
export default Vue.extend({
  name: "ModelLogs",
  components: { Typography },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>

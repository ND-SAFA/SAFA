<template>
  <v-container>
    <v-row>
      <h1>{{ project.name }}</h1></v-row
    >
    <v-row class="text-caption mt-5">{{ project.description }}</v-row>
    <v-row>
      <v-divider />
    </v-row>
    <v-row class="mt-5"> <h3>Artifacts</h3></v-row>

    <v-row>
      <v-btn
        fab
        x-small
        color="primary"
        class="ma-1"
        v-for="artifact in project.artifacts"
        :key="artifact.name"
        @click="() => underDevelopmentError('artifacts')"
      >
        {{ artifact.name }}
      </v-btn>
      <label class="text-caption" v-if="project.artifacts.length === 0">
        No Artifact Created.
      </label>
    </v-row>
    <v-row>
      <v-divider />
    </v-row>
    <v-row class="mt-5"> <h3>Traces</h3></v-row>
    <v-row>
      <v-btn
        x-small
        color="primary"
        class="ma-1"
        v-for="trace in project.traces"
        :key="`${trace.source}-${trace.target}`"
        @click="() => underDevelopmentError('traces')"
      >
        {{ trace.source }}-{{ trace.target }}
      </v-btn>
      <label class="text-caption" v-if="project.traces.length === 0">
        No Traces Created.
      </label>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { appModule } from "@/store";
import { Project } from "@/types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
  methods: {
    underDevelopmentError(type: "artifact" | "trace"): void {
      appModule.onWarning(
        `View more details on ${type} selected is under development `
      );
    },
  },
});
</script>

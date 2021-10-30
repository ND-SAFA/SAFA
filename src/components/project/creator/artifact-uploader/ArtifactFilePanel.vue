<template>
  <FilePanel
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    :errors="errors"
  >
    <template v-slot:title>
      <h3>{{ artifactFile.type }}</h3>
    </template>

    <template v-slot:after-rows>
      <v-container>
        <v-row><h4>Parsed Artifacts</h4> </v-row>
        <v-row v-if="artifactFile.artifacts !== undefined">
          <v-btn
            fab
            x-small
            color="primary"
            class="ma-1"
            v-for="artifact in artifactFile.artifacts"
            :key="artifact.name"
            @click="underDevelopmentError()"
          >
            {{ artifact.name }}
          </v-btn>
        </v-row>
        <v-row v-else>
          <label class="text-caption"> No Artifacts have been parseed. </label>
        </v-row>
      </v-container>
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactFile } from "@/types/common-components";
import FilePanel from "@/components/project/creator/shared/FilePanel.vue";
import { appModule } from "@/store";

export default Vue.extend({
  components: {
    FilePanel,
  },
  props: {
    artifactFile: {
      type: Object as PropType<ArtifactFile>,
      required: true,
    },
  },
  computed: {
    isValid(): boolean {
      return this.artifactFile.file !== undefined;
    },
    errors(): string[] {
      return this.artifactFile.errors === undefined
        ? []
        : this.artifactFile.errors;
    },
  },
  methods: {
    onChange(file: File): void {
      this.$emit("onChange", { ...this.artifactFile, file });
    },

    emitValidationState(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
    underDevelopmentError(): void {
      appModule.onWarning("Viewing parsed artifacts is under development.");
    },
  },
  watch: {
    isValid(): void {
      this.emitValidationState();
    },
  },
  mounted() {
    this.emitValidationState();
  },
});
</script>

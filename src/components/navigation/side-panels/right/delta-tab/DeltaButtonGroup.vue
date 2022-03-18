<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <h2 class="text-h6">{{ title }}</h2>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <artifact-delta-button
        v-for="(name, nameIndex) in names"
        class="mr-1 mb-1"
        :key="name"
        :name="name"
        :deltaType="deltaType"
        @click="$emit('click', ids[nameIndex])"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DeltaType } from "@/types";
import { capitalize } from "@/util";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

/**
 * Displays delta buttons.
 *
 * @emits `click` - On delta button click.
 */
export default Vue.extend({
  components: { ArtifactDeltaButton },
  props: {
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
    names: {
      type: Array as PropType<string[]>,
      required: true,
    },
    ids: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  data() {
    return {
      isDeltaOpen: false,
      selectedName: undefined as string | undefined,
    };
  },
  methods: {
    closeDeltaModal(): void {
      this.selectedName = undefined;
      this.isDeltaOpen = false;
    },
    selectArtifact(artifactName: string): void {
      this.selectedName = artifactName;
      this.isDeltaOpen = true;
    },
  },
  computed: {
    title(): string {
      return capitalize(this.deltaType);
    },
  },
});
</script>

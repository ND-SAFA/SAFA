<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <h2 class="text-h6">{{ title }}</h2>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <artifact-delta-button
        v-for="{ name, id } in artifacts"
        class="mr-1 mb-1"
        :key="name"
        :name="name"
        :deltaType="deltaType"
        @click="$emit('click', id)"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, DeltaType } from "@/types";
import { capitalize } from "@/util";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

/**
 * Displays a group of delta buttons.
 *
 * @emits `click` - On delta button click.
 */
export default Vue.extend({
  name: "DeltaButtonGroup",
  components: { ArtifactDeltaButton },
  props: {
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
    artifacts: {
      type: Array as PropType<Artifact[]>,
      required: true,
    },
  },
  data() {
    return {
      selectedName: undefined as string | undefined,
    };
  },
  methods: {
    /**
     * Selects the given artifact.
     * @param artifactName - The artifact to select.
     */
    selectArtifact(artifactName: string): void {
      this.selectedName = artifactName;
    },
  },
  computed: {
    /**
     * @return The button group title.
     */
    title(): string {
      return capitalize(this.deltaType);
    },
  },
});
</script>

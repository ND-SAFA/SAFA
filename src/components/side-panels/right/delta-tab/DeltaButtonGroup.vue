<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <h3>{{ title }}</h3>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <ArtifactDeltaButton
        v-for="(artifact, name) in artifacts"
        :key="name"
        :artifact="artifact"
        :name="name"
        :deltaType="deltaType"
        @onClick="$emit('onArtifactClick', $event)"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import { DeltaArtifact, DeltaType } from "@/types/domain/delta";
import Vue, { PropType } from "vue";
import ArtifactDeltaButton from "@/components/side-panels/right/delta-tab/ArtifactDeltaButton.vue";
import { capitalize } from "@/util/string-helper";

export default Vue.extend({
  components: { ArtifactDeltaButton },
  props: {
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
    artifacts: {
      type: Object as PropType<Record<string, DeltaArtifact>>,
      required: true,
    },
  },
  data() {
    return {
      isDeltaOpen: false,
      selectedArtifact: undefined as DeltaArtifact | undefined,
      selectedName: undefined as string | undefined,
    };
  },
  methods: {
    closeDeltaModal(): void {
      this.selectedArtifact = undefined;
      this.selectedName = undefined;
      this.isDeltaOpen = false;
    },
    selectArtifact(artifactName: string): void {
      this.selectedArtifact = this.artifacts[artifactName];
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

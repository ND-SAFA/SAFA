<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <typography :value="title" />
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <artifact-delta-button
        v-for="{ name, id } in itemFields"
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
import { Artifact, DeltaType, EntityModification, TraceLink } from "@/types";
import { capitalize } from "@/util";
import { Typography } from "@/components/common";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

/**
 * Displays a group of delta buttons.
 *
 * @emits `click` - On delta button click.
 */
export default Vue.extend({
  name: "DeltaButtonGroup",
  components: { Typography, ArtifactDeltaButton },
  props: {
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
    items: {
      type: Object as PropType<
        Record<string, Artifact | EntityModification<Artifact> | TraceLink>
      >,
      required: true,
    },
    // If true, items will be interpreted as traces instead of artifacts.
    isTraces: Boolean,
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
     * @return The number of items.
     */
    itemCount(): number {
      return Object.keys(this.items).length;
    },
    /**
     * @return The button group title.
     */
    title(): string {
      return `${this.itemCount} ${capitalize(this.deltaType)}`;
    },
    itemFields(): { id: string; name: string }[] {
      const items = Object.values(this.items);

      if (this.isTraces) {
        return (items as TraceLink[]).map(
          ({ traceLinkId, sourceName, targetName }) => ({
            id: traceLinkId,
            name: `${sourceName} > ${targetName}`,
          })
        );
      } else {
        return this.deltaType === "modified"
          ? (items as EntityModification<Artifact>[]).map(
              ({ after: { id, name } }) => ({ id, name })
            )
          : (items as Artifact[]).map(({ id, name }) => ({ id, name }));
      }
    },
  },
});
</script>

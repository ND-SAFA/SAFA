<template>
  <toggle-list :value="itemFields.length > 0" :title="title">
    <artifact-delta-button
      v-for="{ name, id } in itemFields"
      :key="name"
      :name="name"
      :delta-type="deltaType"
      @click="$emit('click', id)"
    />
  </toggle-list>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import {
  ArtifactSchema,
  DeltaType,
  EntityModification,
  TraceLinkSchema,
} from "@/types";
import { capitalize } from "@/util";
import { ToggleList } from "@/components/common";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

/**
 * Displays a group of delta buttons.
 *
 * @emits `click` (String) - On delta button click.
 */
export default defineComponent({
  name: "DeltaButtonGroup",
  components: { ArtifactDeltaButton, ToggleList },
  props: {
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
    items: {
      type: Object as PropType<
        Record<
          string,
          ArtifactSchema | EntityModification<ArtifactSchema> | TraceLinkSchema
        >
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
        return (items as TraceLinkSchema[]).map(
          ({ traceLinkId, sourceName, targetName }) => ({
            id: traceLinkId,
            name: `${sourceName} > ${targetName}`,
          })
        );
      } else {
        return this.deltaType === "modified"
          ? (items as EntityModification<ArtifactSchema>[]).map(
              ({ after: { id, name } }) => ({ id, name })
            )
          : (items as ArtifactSchema[]).map(({ id, name }) => ({ id, name }));
      }
    },
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
});
</script>

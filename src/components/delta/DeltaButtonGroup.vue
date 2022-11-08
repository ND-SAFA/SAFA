<template>
  <toggle-list :value="itemFields.length > 0" :title="title">
    <artifact-delta-button
      v-for="{ name, id } in itemFields"
      class="mr-1 mt-1"
      :key="name"
      :name="name"
      :deltaType="deltaType"
      @click="$emit('click', id)"
    />
  </toggle-list>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactModel,
  DeltaType,
  EntityModification,
  TraceLinkModel,
} from "@/types";
import { capitalize } from "@/util";
import { ToggleList } from "@/components/common";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

/**
 * Displays a group of delta buttons.
 *
 * @emits `click` - On delta button click.
 */
export default Vue.extend({
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
          ArtifactModel | EntityModification<ArtifactModel> | TraceLinkModel
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
        return (items as TraceLinkModel[]).map(
          ({ traceLinkId, sourceName, targetName }) => ({
            id: traceLinkId,
            name: `${sourceName} > ${targetName}`,
          })
        );
      } else {
        return this.deltaType === "modified"
          ? (items as EntityModification<ArtifactModel>[]).map(
              ({ after: { id, name } }) => ({ id, name })
            )
          : (items as ArtifactModel[]).map(({ id, name }) => ({ id, name }));
      }
    },
  },
});
</script>

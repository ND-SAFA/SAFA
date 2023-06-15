<template>
  <expansion-item
    :model-value="itemFields.length > 0"
    :label="title"
    :class="className"
  >
    <artifact-delta-button
      v-for="{ name, id } in itemFields"
      :key="name"
      :name="name"
      :delta-type="props.deltaType"
      @click="emit('click', id)"
    />
  </expansion-item>
</template>

<script lang="ts">
/**
 * Displays a group of delta buttons.
 */
export default {
  name: "DeltaButtonGroup",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  ArtifactSchema,
  EntityModification,
  TraceLinkSchema,
  DeltaType,
  SelectOption,
} from "@/types";
import { capitalize, getEnumColor } from "@/util";
import { deltaStore, useTheme } from "@/hooks";
import { ExpansionItem } from "@/components/common";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

const props = defineProps<{
  /**
   * The change type for this group.
   */
  deltaType: DeltaType;
  /**
   * A collection of all items with this type of change, keyed by id.
   */
  items: Record<
    string,
    ArtifactSchema | EntityModification<ArtifactSchema> | TraceLinkSchema
  >;
  /**
   *  If true, items will be interpreted as traces instead of artifacts.
   */
  isTraces?: boolean;
}>();

const emit = defineEmits<{
  (e: "click", id: string): void;
}>();

const { darkMode } = useTheme();

const itemCount = computed(() => Object.keys(props.items).length);
const title = computed(
  () => `${itemCount.value} ${capitalize(props.deltaType)}`
);

const className = computed(
  () =>
    `rounded q-mb-sm bd-${getEnumColor(props.deltaType)}` +
    (darkMode.value ? "" : ` bg-${props.deltaType}`)
);

const itemFields = computed<SelectOption[]>(() => {
  const items = Object.values(props.items);

  if (props.isTraces) {
    return (items as TraceLinkSchema[]).map(
      ({ traceLinkId, sourceName, targetName }) => ({
        id: traceLinkId,
        name: `${sourceName} > ${targetName}`,
      })
    );
  } else {
    return props.deltaType === "modified"
      ? (items as EntityModification<ArtifactSchema>[]).map(
          ({ after: { id, name } }) => ({ id, name })
        )
      : (items as ArtifactSchema[]).map(({ id, name }) => ({ id, name }));
  }
});
</script>

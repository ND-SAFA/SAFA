<template>
  <expansion-item
    :model-value="itemFields.length > 0"
    :label="title"
    :class="className"
    style="border-width: 0 0 0 2px !important; border-radius: 0 !important"
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
  EntityModificationSchema,
  TraceLinkSchema,
  SelectOption,
  ArtifactDeltaButtonGroupProps,
} from "@/types";
import { capitalize, getEnumColor } from "@/util";
import { ExpansionItem } from "@/components/common";
import ArtifactDeltaButton from "./ArtifactDeltaButton.vue";

const props = defineProps<ArtifactDeltaButtonGroupProps>();

const emit = defineEmits<{
  (e: "click", id: string): void;
}>();

const itemCount = computed(() => Object.keys(props.items).length);
const title = computed(
  () => `${itemCount.value} ${capitalize(props.deltaType)}`
);

const className = computed(() => `q-mb-sm bd-${getEnumColor(props.deltaType)}`);

/**
 * Converts all delta artifacts and traces into a list of select options.
 */
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
      ? (items as EntityModificationSchema<ArtifactSchema>[]).map(
          ({ after: { id, name } }) => ({ id, name })
        )
      : (items as ArtifactSchema[]).map(({ id, name }) => ({ id, name }));
  }
});
</script>

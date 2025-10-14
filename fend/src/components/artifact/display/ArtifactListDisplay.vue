<template>
  <q-virtual-scroll
    v-slot="{ item }: { item: ArtifactSchema }"
    :items="props.artifacts"
    style="max-height: 300px"
    :data-cy="props.dataCy"
  >
    <list-item
      :key="item.id"
      clickable
      :action-cols="props.actionCols"
      :data-cy="props.itemDataCy"
      @click="emit('click', item)"
    >
      <artifact-body-display
        display-title
        :artifact="item"
        :full-width="props.fullWidth"
      />
      <template v-if="!!slots.actions" #actions>
        <slot name="actions" :artifact="item" />
      </template>
    </list-item>
  </q-virtual-scroll>
</template>

<script lang="ts">
/**
 * Displays a list of artifacts.
 */
export default {
  name: "ArtifactListDisplay",
};
</script>

<script setup lang="ts">
import { useSlots } from "vue";
import { ArtifactListProps, ArtifactSchema } from "@/types";
import { ArtifactBodyDisplay, ListItem } from "@/components";

const props = defineProps<ArtifactListProps>();

const emit = defineEmits<{
  (e: "click", artifact: ArtifactSchema): void;
}>();

const slots = useSlots();
</script>

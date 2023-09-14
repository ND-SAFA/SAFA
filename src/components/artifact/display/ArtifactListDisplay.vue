<template>
  <list :scroll-height="300" :data-cy="props.dataCy">
    <q-virtual-scroll
      v-slot="{ item }: { item: ArtifactSchema }"
      :items="props.artifacts"
      style="max-height: 300px"
    >
      <list-item
        :key="item.id"
        clickable
        :action-cols="props.actionCols"
        :data-cy="props.itemDataCy"
        @click="emit('click', item)"
      >
        <artifact-body-display display-title :artifact="item" />
        <template v-if="!!slots.actions" #actions>
          <slot name="actions" :artifact="item" />
        </template>
      </list-item>
    </q-virtual-scroll>
  </list>
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
import { ArtifactSchema } from "@/types";
import { ArtifactBodyDisplay, List, ListItem } from "@/components";

const props = defineProps<{
  artifacts: ArtifactSchema[];
  dataCy?: string;
  itemDataCy?: string;
  actionCols?: number;
}>();

const emit = defineEmits<{
  (e: "click", artifact: ArtifactSchema): void;
}>();

const slots = useSlots();
</script>

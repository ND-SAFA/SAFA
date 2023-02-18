<template>
  <q-item
    :clickable="props.clickable"
    style="max-width: 500px"
    @click="emit('click')"
  >
    <q-item-section>
      <q-item-label>
        <flex-box align="center" justify="between">
          <typography :value="props.artifact.name" />
          <attribute-chip artifact-type :value="artifactType" />
        </flex-box>
        <q-separator v-if="!!props.displayDivider" class="q-mt-sm" />
      </q-item-label>
      <q-item-label caption>
        <typography
          secondary
          variant="expandable"
          :value="props.artifact.body"
          :default-expanded="!!props.displayDivider && !!props.displayTitle"
        />
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
/**
 * Displays the body of an artifact that can be expanded.
 */
export default {
  name: "ArtifactBodyDisplay",
};
</script>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { ArtifactSchema } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import { AttributeChip } from "./attribute";
import Typography from "./Typography.vue";

const props = defineProps<{
  artifact: ArtifactSchema;
  displayTitle?: boolean;
  displayDivider?: boolean;
  clickable?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const artifactType = computed(() =>
  typeOptionsStore.getArtifactTypeDisplay(props.artifact.type)
);
</script>

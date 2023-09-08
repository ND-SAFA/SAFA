<template>
  <q-splitter v-if="showSummary" v-model="splitterModel" :horizontal="!isCode">
    <template #before>
      <div>
        <typography variant="caption" value="Summary" />
        <typography
          variant="expandable"
          :value="props.artifact.summary"
          default-expanded
          :collapse-length="0"
        />
      </div>
    </template>
    <template #after>
      <div class="q-ml-md">
        <typography variant="caption" value="Content" />
        <typography
          :variant="isCode ? 'code' : 'expandable'"
          :value="props.artifact.body"
          :default-expanded="!isCode"
        />
      </div>
    </template>
  </q-splitter>
  <div v-else>
    <typography variant="caption" value="Content" />
    <typography
      :variant="isCode ? 'code' : 'expandable'"
      :value="props.artifact.body"
      :default-expanded="!isCode"
    />
  </div>
</template>

<script lang="ts">
/**
 * Displays both the body and summary of an artifact.
 * If no summary exists, only the artifact body is displayed.
 */
export default {
  name: "ArtifactContentDisplay",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactProps } from "@/types";
import { Typography } from "@/components/common";

const props = defineProps<ArtifactProps>();

const splitterModel = ref(40);

const showSummary = computed(() => !!props.artifact.summary);
const isCode = computed(() => props.artifact.isCode);
</script>

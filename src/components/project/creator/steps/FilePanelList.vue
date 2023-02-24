<template>
  <div>
    <file-format-alert />

    <list bordered class="q-my-lg">
      <file-panel
        v-for="(panel, idx) in panels"
        :key="idx"
        :panel="panel"
        :label="props.label"
        @panel:delete="emit('panel:delete', idx)"
      >
        <template #panel>
          <slot name="panel" :panel="panel" />
        </template>
      </file-panel>
    </list>

    <flex-box justify="center">
      <text-button
        text
        icon="add"
        :label="newLabel"
        @click="emit('panel:add')"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading files.
 */
export default {
  name: "FilePanelList",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { CreatorFilePanel } from "@/types";
import {
  TextButton,
  FlexBox,
  FileFormatAlert,
  List,
} from "@/components/common";
import FilePanel from "./FilePanel.vue";

const props = defineProps<{
  panels: CreatorFilePanel[];
  label: string;
}>();

const emit = defineEmits<{
  (e: "panel:add"): void;
  (e: "panel:delete", index: number): void;
}>();

const newLabel = computed(() => `New ${props.label}`);
</script>

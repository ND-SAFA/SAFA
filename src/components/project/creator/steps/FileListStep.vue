<template>
  <div>
    <file-format-alert />

    <list bordered class="q-my-lg">
      <expansion-item
        v-for="(panel, idx) in panels"
        :key="idx"
        v-model="panel.open"
        :label="panel.name || newLabel"
        :caption="props.label"
      >
        <div class="q-mx-md">
          <slot name="panel" :panel="panel" />
          <file-input v-model="panel.file" />
          <flex-box justify="between">
            <switch-input
              v-model="panel.ignoreErrors"
              label="Ignore Errors"
              color="grey"
            />
            <text-button
              icon="delete"
              label="Delete"
              @click="emit('panel:delete', idx)"
            />
          </flex-box>
        </div>
      </expansion-item>
    </list>

    <flex-box justify="center">
      <text-button icon="add" :label="newLabel" @click="emit('panel:add')" />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading files.
 */
export default {
  name: "FileListStep",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  ExpansionItem,
  FileInput,
  SwitchInput,
  TextButton,
  FlexBox,
  FileFormatAlert,
  List,
} from "@/components/common";

const props = defineProps<{
  panels: {
    name: string;
    open: boolean;
    ignoreErrors: boolean;
    file: File | undefined;
  }[];
  label: string;
}>();

const emit = defineEmits<{
  (e: "panel:add"): void;
  (e: "panel:delete", index: number): void;
}>();

const newLabel = computed(() => `New ${props.label}`);
</script>

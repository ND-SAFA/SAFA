<template>
  <expansion-item
    v-model="panel.open"
    :label="panel.name || newLabel"
    :caption="props.label"
  >
    <div class="q-mx-md">
      <slot name="panel" :panel="panel" />
      <file-input v-model="panel.file" :multiple="false" />
      <flex-box full-width justify="between">
        <switch-input
          v-model="panel.ignoreErrors"
          label="Ignore Errors"
          color="grey"
        />
        <typography
          v-if="!panel.ignoreErrors && !!panel.errorMessage"
          :value="panel.errorMessage"
          color="negative"
        />
      </flex-box>
      <flex-box justify="end">
        <text-button
          icon="delete"
          label="Delete"
          @click="emit('panel:delete')"
        />
      </flex-box>
    </div>
  </expansion-item>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading a file.
 */
export default {
  name: "FilePanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { CreatorFilePanel } from "@/types";
import {
  ExpansionItem,
  FileInput,
  SwitchInput,
  TextButton,
  FlexBox,
  Typography,
} from "@/components/common";

const props = defineProps<{
  panel: CreatorFilePanel;
  label: string;
}>();

const emit = defineEmits<{
  (e: "panel:delete"): void;
}>();

const newLabel = computed(() => `New ${props.label}`);
</script>

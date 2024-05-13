<template>
  <details-panel panel="editTrace" data-cy="panel-trace-edit">
    <template #actions>
      <text-button
        text
        label="View Trace Link"
        icon="trace"
        data-cy="button-trace-view"
        @click="appStore.openDetailsPanel('displayTrace')"
      />
    </template>
    <panel-card title="Save Trace Link" borderless>
      <text-input
        v-model="editTraceStore.editedTrace.explanation"
        label="Explanation"
        type="textarea"
      />
      <template #actions>
        <flex-box full-width justify="end">
          <text-button
            label="Save"
            icon="save"
            color="primary"
            :loading="traceApiStore.editLoading"
            data-cy="button-trace-edit"
            @click="handleSubmit"
          />
        </flex-box>
      </template>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for editing trace links.
 */
export default {
  name: "EditTraceLinkPanel",
};
</script>

<script setup lang="ts">
import { appStore, traceApiStore, editTraceStore } from "@/hooks";
import {
  FlexBox,
  PanelCard,
  TextButton,
  DetailsPanel,
  TextInput,
} from "@/components/common";

/**
 * Creates a trace link from the given artifacts.
 */
async function handleSubmit(): Promise<void> {
  await traceApiStore.handleEdit(editTraceStore.editedTrace, {
    onSuccess: () => {
      appStore.closeSidePanels();
      editTraceStore.resetTrace(undefined);
    },
  });
}
</script>

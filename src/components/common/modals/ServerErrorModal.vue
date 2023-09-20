<template>
  <modal title="Server Errors" :open="open" @close="handleClose">
    <list>
      <list-item v-for="error in props.errors" :key="error">
        <code class="text-word-break-all">
          {{ error }}
        </code>
      </list-item>
    </list>
  </modal>
</template>

<script lang="ts">
/**
 * Renders server errors.
 */
export default {
  name: "ServerErrorModal",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ErrorModalProps } from "@/types";
import { appStore } from "@/hooks";
import { List, ListItem } from "@/components/common/display";
import Modal from "./Modal.vue";

const props = defineProps<ErrorModalProps>();

const open = computed(() => appStore.popups.errorModal);

/**
 * Closes the error display.
 */
function handleClose() {
  appStore.toggle("errorModal");
}
</script>

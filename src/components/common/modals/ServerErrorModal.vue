<template>
  <modal
    title="Server Errors"
    :isOpen="isOpen"
    :actionsHeight="0"
    :isLoading="isLoading"
    @close="handleClose"
  >
    <template v-slot:body>
      <v-list disabled>
        <v-list-item v-for="(error, errorIndex) in errors" :key="errorIndex">
          <v-list-item-content class="pa-0">
            <code style="word-break: break-all">
              {{ error }}
            </code>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { appStore } from "@/hooks";
import Modal from "./Modal.vue";

/**
 * Renders server errors.
 */
export default Vue.extend({
  name: "ServerErrorModal",
  components: {
    Modal,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  props: {
    isOpen: Boolean,
    errors: Array as PropType<string[]>,
  },
  methods: {
    handleClose() {
      appStore.toggleErrorDisplay();
    },
  },
});
</script>

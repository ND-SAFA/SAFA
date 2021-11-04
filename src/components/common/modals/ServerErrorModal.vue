<template>
  <GenericModal
    title="Server Errors"
    :isOpen="isOpen"
    :actionsHeight="0"
    :isLoading="isLoading"
    @onClose="onClose"
  >
    <template v-slot:body>
      <code
        v-for="(error, errorIndex) in errors"
        :key="errorIndex"
        justify="left"
      >
        <b>{{ errorIndex }}:</b>
        <p>{{ error }}</p>
      </code>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import { appModule } from "@/store";
import { PanelType } from "@/types/store";

export default Vue.extend({
  components: {
    GenericModal,
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
    onClose() {
      appModule.closePanel(PanelType.errorDisplay);
    },
  },
});
</script>

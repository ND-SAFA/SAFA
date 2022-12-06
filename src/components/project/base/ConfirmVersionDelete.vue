<template>
  <generic-modal
    size="xxs"
    :is-open="deleteDialogue"
    :title="title"
    data-cy="modal-version-delete"
    :actions-height="0"
    @close="handleCancel"
  >
    <template v-slot:body>
      <v-btn
        color="error"
        @click="handleConfirm"
        block
        class="mt-3"
        data-cy="button-version-delete"
      >
        Delete
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { GenericModal } from "@/components/common";

/**
 * A modal for confirming version deletion.
 *
 * @emits-1 `confirm` (ProjectVersion) - On delete confirm.
 * @emits-2 `cancel` - On delete cancel.
 */
export default Vue.extend({
  name: "ConfirmVersionDelete",
  components: { GenericModal },
  props: {
    deleteDialogue: {
      type: Boolean,
      required: true,
    },
    version: {
      type: Object as PropType<VersionSchema>,
      required: false,
    },
  },
  data() {
    return {
      title: "",
    };
  },
  methods: {
    /**
     * Emits a request to confirm the deletion.
     */
    handleConfirm() {
      this.$emit("confirm", this.version);
    },
    /**
     * Emits a request to cancel the deletion.
     */
    handleCancel() {
      this.$emit("cancel");
    },
  },
  watch: {
    /**
     * Updates the title when the version changes.
     */
    version(version: VersionSchema) {
      this.title = `Delete version: ${versionToString(version)}`;
    },
  },
});
</script>

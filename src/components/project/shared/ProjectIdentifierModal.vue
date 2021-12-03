<template>
  <generic-modal
    :is-open="isOpen"
    :title="title"
    size="s"
    :actions-height="50"
    :is-loading="isLoading"
    @close="onClose"
  >
    <template v-slot:body>
      <project-identifier-input
        v-bind:name.sync="name"
        v-bind:description.sync="description"
      />
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn @click="onSave" color="primary">
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier } from "@/types";
import { GenericModal } from "@/components/common";
import { ProjectIdentifierInput } from "@/components/project/shared";

export default Vue.extend({
  components: {
    GenericModal,
    ProjectIdentifierInput,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
    title: {
      type: String,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      name: "",
      description: "",
    };
  },
  mounted() {
    this.clearData();
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (!isOpen) {
        this.clearData();
      }
    },
    project(project: ProjectIdentifier | undefined): void {
      if (project !== undefined) {
        this.name = project.name;
        this.description = project.description;
      }
    },
  },
  methods: {
    clearData() {
      this.name = "";
      this.description = "";
    },
    onClose() {
      this.$emit("onClose");
    },
    onSave() {
      const projectId = this.project?.projectId || "";
      this.$emit("onSave", {
        projectId: projectId,
        name: this.name,
        description: this.description,
      } as ProjectIdentifier);
    },
  },
});
</script>

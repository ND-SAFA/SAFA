<template>
  <GenericModal
    :isOpen="isOpen"
    :width="500"
    :title="title"
    :actionsHeight="50"
    @onClose="onClose"
  >
    <template v-slot:body>
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-text-field v-model="name" label="Project Name" required />
          </v-col>

          <v-col cols="6">
            <v-text-field
              v-model="description"
              label="Project description"
              required
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
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
  </GenericModal>
</template>

<script lang="ts">
import { ProjectIdentifier } from "@/types/domain/project";
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";

export default Vue.extend({
  components: {
    GenericModal,
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
    project(newProject: ProjectIdentifier) {
      this.name = newProject.name;
      this.description = newProject.description;
    },
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
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
      const project: ProjectIdentifier | undefined = this.$props.project;
      const projectId = project === undefined ? "" : project.projectId;

      this.$emit("onSave", {
        projectId: projectId,
        name: this.name,
        description: this.description,
      } as ProjectIdentifier);
    },
  },
});
</script>

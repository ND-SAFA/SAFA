<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col cols="9">
          <h1>{{ project.name }}</h1></v-col
        >
        <v-col cols="3">
          <generic-icon-button
            tooltip="Edit title"
            icon-id="mdi-pencil"
            @click="onEdit"
          />
        </v-col>
      </v-row>
      <v-divider />
      <p>
        {{ hasDescription ? project.description : emptyDescriptionMessage }}
      </p>
    </v-col>
    <project-identifier-modal
      title="Edit Project"
      :is-open="isEditOpen"
      v-bind:project.sync="projectToEdit"
      :is-loading="isEditLoading"
      @onClose="isEditOpen = false"
      @onSave="onSave"
    />
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectIdentifier } from "@/types";
import { GenericIconButton } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";
import { saveOrUpdateProject } from "@/api";
import { projectModule } from "@/store";

const EMPTY_DESCRIPTION_MESSAGE = "Project contains empty description";
/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  components: { GenericIconButton, ProjectIdentifierModal },
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
    emptyDescriptionMessage: {
      type: String,
      required: false,
      default: EMPTY_DESCRIPTION_MESSAGE,
    },
  },
  data() {
    return {
      isEditLoading: false,
      isEditOpen: false,
      projectToEdit: this.project,
    };
  },
  computed: {
    hasDescription(): boolean {
      const description = this.project.description;
      return description !== "";
    },
  },
  methods: {
    onEdit(): void {
      this.projectToEdit = this.project;
      this.isEditOpen = true;
    },
    onSave(project: ProjectIdentifier): void {
      this.isEditLoading = true;
      saveOrUpdateProject({
        projectId: this.project.projectId,
        name: project.name,
        description: project.description,
        artifacts: [],
        traces: [],
      })
        .then(() => projectModule.SAVE_PROJECT_IDENTIFIER(project))
        .catch((e) => {
          console.error(e);
        })
        .finally(() => {
          this.isEditLoading = false;
          this.isEditOpen = false;
        });
    },
  },
});
</script>

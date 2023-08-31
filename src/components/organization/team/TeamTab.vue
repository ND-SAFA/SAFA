<template>
  <panel-card title="Teams" :subtitle="subtitle">
    <template #title-actions>
      <text-button
        v-if="addMode"
        text
        label="Cancel"
        icon="cancel"
        @click="handleClose"
      />
    </template>

    <stepper
      v-model="currentStep"
      hide-actions
      :steps="steps"
      data-cy="team-stepper"
    >
      <template #1>
        <selector-table
          v-if="!addMode"
          v-model:selected="selectedTeams"
          addable
          deletable
          :columns="teamColumns"
          :rows="rows"
          :loading="loading"
          row-key="id"
          item-name="team"
        >
          <template #cell-actions="{ row }">
            <icon-button
              v-if="displayLeave(row)"
              icon="leave"
              tooltip="Leave team"
              data-cy="button-selector-leave"
              @click="handleLeave(row)"
            />
          </template>
        </selector-table>
      </template>
      <template #2>
        <typography variant="subtitle" el="h3" :value="steps[1].title" />
        <separator b="2" />
        <expansion-item default-opened label="Members">
          <team-member-table />
        </expansion-item>
        <expansion-item label="Projects">
          <project-selector-table :open="currentStep === 2" />
        </expansion-item>
      </template>
    </stepper>
  </panel-card>
</template>

<script lang="ts">
/**
 * A tab for managing teams within an organization.
 */
export default {
  name: "TeamTab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { StepperStep, TeamSchema } from "@/types";
import { teamColumns } from "@/util";
import {
  memberApiStore,
  membersStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import {
  PanelCard,
  TextButton,
  IconButton,
  Stepper,
  SelectorTable,
  ExpansionItem,
  Typography,
  Separator,
} from "@/components/common";
import { TeamMemberTable } from "@/components/members";
import { ProjectSelectorTable } from "@/components/project";

const defaultTeamListStep = (): StepperStep => ({
  title: "Teams",
  done: false,
});

const defaultTeamStep = (): StepperStep => ({
  title: "Select a Team",
  done: false,
});

const currentStep = ref(1);
const steps = ref<StepperStep[]>([defaultTeamListStep(), defaultTeamStep()]);
const selectedTeam = ref<TeamSchema>();

const loading = ref(false);
const addMode = ref(false);

const rows: TeamSchema[] = [
  {
    id: "1",
    name: "Team 1",
    members: membersStore.members,
    projects: [projectStore.projectIdentifier],
  },
  {
    id: "2",
    name: "Team 2",
    members: membersStore.members,
    projects: [projectStore.projectIdentifier],
  },
];

const selectedTeams = computed({
  get() {
    return selectedTeam.value ? [selectedTeam.value] : [];
  },
  set(teams: TeamSchema[]) {
    selectedTeam.value = teams[0];

    if (teams[0]) {
      currentStep.value = 2;
      steps.value[0].done = true;
      steps.value[1] = {
        title: teams[0].name,
        done: false,
      };
    } else {
      steps.value = [defaultTeamListStep(), defaultTeamStep()];
    }
  },
});

const subtitle = computed(() =>
  addMode.value ? "Create a new team." : "Manage teams and permissions."
);

/**
 * Closes the add team form and resets entered data.
 */
function handleClose() {
  addMode.value = false;
}

/**
 * Whether to display the leave button for a team.
 */
function displayLeave(team: TeamSchema): boolean {
  const member = team.members.find(
    ({ email }) => email === sessionStore.userEmail
  );

  return !!member && team.members.length > 1;
}

/**
 * Leaves the selected team.
 */
function handleLeave(team: TeamSchema) {
  const member = team.members.find(
    ({ email }) => email === sessionStore.userEmail
  );

  if (!member) return;

  memberApiStore.handleDelete(member);
}
</script>

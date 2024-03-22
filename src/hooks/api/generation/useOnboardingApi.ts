import { defineStore } from "pinia";

import { OnboardingApiHook, OnboardingStatusSchema } from "@/types";
import { ARTIFACT_GENERATION_ONBOARDING, ONBOARDING_STEPS } from "@/util";
import {
  artifactGenerationApiStore,
  artifactStore,
  billingApiStore,
  createProjectApiStore,
  getVersionApiStore,
  gitHubApiStore,
  integrationsStore,
  jobApiStore,
  logStore,
  onboardingStore,
  permissionStore,
  projectApiStore,
  projectStore,
  setProjectApiStore,
  useApi,
} from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { getOnboardingStatus, setOnboardingStatus } from "@/api";
import { pinia } from "@/plugins";

/**
 * This store manages interactions with the onboarding API.
 */
export const useOnboardingApi = defineStore(
  "onboardingApi",
  (): OnboardingApiHook => {
    const onboardingApi = useApi("onboardingApi");

    async function handleLoadOnboardingProject(): Promise<void> {
      if (onboardingStore.projectId) {
        // If a project ID is stored, load that.
        await getVersionApiStore.handleLoadCurrent(
          { projectId: onboardingStore.projectId },
          {
            onError: () => {
              onboardingStore.projectId = "";
              onboardingStore.error = true;
            },
          }
        );
      } else if (onboardingStore.uploadedJob?.completedEntityId) {
        // If we only have the upload job's version ID, load that.
        await getVersionApiStore.handleLoad(
          onboardingStore.uploadedJob?.completedEntityId
        );
      }
    }

    async function handleGetOnboardingStatus(open?: boolean): Promise<void> {
      await onboardingApi.handleRequest(() => getOnboardingStatus(), {
        onSuccess: (status) => {
          // Open the onboarding workflow if it has not yet been completed, or is manually opened.
          onboardingStore.projectId = status.projectId || null;
          onboardingStore.open = open || !status.completed;
        },
      });
    }

    async function handleUpdateOnboardingStatus(
      status: OnboardingStatusSchema
    ): Promise<void> {
      await onboardingApi.handleRequest(() => setOnboardingStatus(status));
    }

    async function handleCloseOnboarding(
      openTo?: "export" | "view"
    ): Promise<void> {
      const resetProject = !!openTo;

      if (openTo === "export") {
        await handleLoadOnboardingProject();
        await projectApiStore.handleDownload("csv");
        logStore.onSuccess("Your data is being exported.");
      } else if (openTo === "view") {
        await handleLoadOnboardingProject();
        await navigateTo(Routes.ARTIFACT, {
          projectId: onboardingStore.projectId,
        });
      }

      onboardingStore.open = false;

      await handleUpdateOnboardingStatus({
        completed: true,
        projectId: resetProject ? "" : onboardingStore.projectId || "",
      });
    }

    async function handleOpenOnboarding(): Promise<void> {
      onboardingStore.projectId = null;
      onboardingStore.open = true;
      onboardingStore.error = false;
      onboardingStore.ignoreCurrentJobs = true;
      onboardingStore.generationCompleted = false;
      onboardingStore.step = 1;
      onboardingStore.steps.forEach((step) => (step.done = false));
      await setProjectApiStore.handleClear();
      await handleUpdateOnboardingStatus({
        completed: false,
        projectId: "",
      });
    }

    async function handleImportAndSummarize(): Promise<void> {
      integrationsStore.gitHubConfig.summarize = true;
      await createProjectApiStore.handleGitHubImport({
        onSuccess: () => {
          jobApiStore.handleReload();
          onboardingStore.ignoreCurrentJobs = false;
        },
        onError: () => (onboardingStore.error = true),
      });
    }

    async function handleEstimateCost(): Promise<void> {
      await handleLoadOnboardingProject();
      await billingApiStore.handleEstimateCost(
        {
          artifacts: artifactStore.allArtifacts.map(({ id }) => id),
          targetTypes: ARTIFACT_GENERATION_ONBOARDING,
        },
        {
          onSuccess: (cost) => (onboardingStore.cost = cost),
          onError: () => (onboardingStore.error = true),
        }
      );
    }

    async function handleGenerateDocumentation(): Promise<void> {
      const credits = onboardingStore.cost?.credits;

      if (!credits) {
        onboardingStore.error = true;
        return;
      }

      if (onboardingStore.displayBilling) {
        await billingApiStore.handleCheckoutSession(
          onboardingStore.cost?.credits || 0,
          `Artifact Generation: ${projectStore.project.name}`
        );
      } else {
        await artifactGenerationApiStore.handleGenerateArtifacts(
          {
            artifacts: artifactStore.allArtifacts.map(({ id }) => id),
            targetTypes: ARTIFACT_GENERATION_ONBOARDING,
          },
          { onError: () => (onboardingStore.error = true) }
        );
      }
    }

    async function handleLoadNextStep(
      currentStep?: keyof typeof ONBOARDING_STEPS
    ): Promise<void> {
      if (currentStep === "connect") {
        integrationsStore.validGitHubCredentials = true;
        await gitHubApiStore.handleLoadProjects();
      } else if (currentStep === "summarize") {
        await handleEstimateCost();
      }

      await onboardingStore.handleNextStep(currentStep);
    }

    async function handleLoadOnboardingState(
      updateState?: "open" | "reset"
    ): Promise<void> {
      // Never load onboarding state in demo mode.
      if (permissionStore.isDemo) return;

      if (updateState === "reset") {
        // Reset all onboarding state.
        await handleOpenOnboarding();
      } else {
        // Load the current onboarding status.
        await handleGetOnboardingStatus(!!updateState);
      }

      // Skip reset if already loading or completed.
      if (!onboardingStore.open || onboardingStore.loading) return;

      onboardingStore.loading = true;

      await gitHubApiStore.handleVerifyCredentials();
      await jobApiStore.handleReload();
      onboardingStore.updateGenerationCompleted();

      if (onboardingStore.skipToRepo) {
        // Skip to "code" step if credentials are set.
        await handleLoadNextStep("connect");
      }
      if (onboardingStore.skipToUpload && updateState !== "reset") {
        // Skip to the "summarize" step if a job has been started, or a project has already been uploaded.
        await handleLoadNextStep("code");
      }
      if (onboardingStore.skipToGenerate && updateState !== "reset") {
        // Skip to the "generate" step if a job has been completed.
        await handleLoadNextStep("summarize");
      }

      onboardingStore.loading = false;
    }

    return {
      handleGetOnboardingStatus,
      handleUpdateOnboardingStatus,
      handleCloseOnboarding,
      handleOpenOnboarding,
      handleImportAndSummarize,
      handleEstimateCost,
      handleGenerateDocumentation,
      handleLoadNextStep,
      handleLoadOnboardingState,
    };
  }
);

export default useOnboardingApi(pinia);

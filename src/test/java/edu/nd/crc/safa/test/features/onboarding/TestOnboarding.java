package edu.nd.crc.safa.test.features.onboarding;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.onboarding.entities.app.OnboardingStateAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.Test;

public class TestOnboarding extends ApplicationBaseTest {

    @Test
    public void testCrud() throws Exception {
        OnboardingStateAppEntity defaultState = getState();
        assertThat(defaultState.isCompleted()).isFalse();
        assertThat(defaultState.getProjectId()).isNull();

        Project project = dbEntityBuilder.newProjectWithReturn("project");

        // Create a second throwaway project, since creating a project updates onboarding state, we
        // need to make sure the project we're setting (within projectVersion) is not the current project_id
        dbEntityBuilder.newProject("throwaway");

        OnboardingStateAppEntity updatedState = updateState(project, true);
        assertThat(updatedState.isCompleted()).isTrue();
        assertThat(updatedState.getProjectId()).isEqualTo(project.getProjectId());
    }

    @Test
    public void testNewProjectUpdatesProjectId() throws Exception {
        OnboardingStateAppEntity defaultState = getState();
        assertThat(defaultState.isCompleted()).isFalse();
        assertThat(defaultState.getProjectId()).isNull();

        Project project = dbEntityBuilder.newProjectWithReturn("project");

        OnboardingStateAppEntity updatedState = getState();
        assertThat(updatedState.isCompleted()).isFalse();
        assertThat(updatedState.getProjectId()).isEqualTo(project.getProjectId());
    }

    private OnboardingStateAppEntity getState() throws Exception {
        return SafaRequest.withRoute(AppRoutes.Onboarding.ROOT)
            .getAsType(new TypeReference<>() {});
    }

    private OnboardingStateAppEntity updateState(Project project, boolean completed) {
        OnboardingStateAppEntity state = new OnboardingStateAppEntity();
        state.setCompleted(completed);
        state.setProjectId(project.getProjectId());
        return SafaRequest.withRoute(AppRoutes.Onboarding.ROOT)
            .putAndParseResponse(state, new TypeReference<>() {});
    }
}

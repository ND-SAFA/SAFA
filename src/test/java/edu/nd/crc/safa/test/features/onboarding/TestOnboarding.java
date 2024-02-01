package edu.nd.crc.safa.test.features.onboarding;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.onboarding.entities.app.OnboardingStateAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
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

        ProjectVersion projectVersion = rootBuilder.getActionBuilder().createProjectWithVersion(getCurrentUser());

        OnboardingStateAppEntity updatedState = updateState(projectVersion.getProject(), true);
        assertThat(updatedState.isCompleted()).isTrue();
        assertThat(updatedState.getProjectId()).isEqualTo(projectVersion.getProject().getProjectId());
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

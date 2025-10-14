package edu.nd.crc.safa.features.onboarding.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.onboarding.entities.db.OnboardingState;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class OnboardingStateAppEntity {
    private boolean completed;
    private UUID projectId;

    public OnboardingStateAppEntity(OnboardingState onboardingState) {
        this.completed = onboardingState.isCompleted();
        this.projectId = onboardingState.getProjectId();
    }
}

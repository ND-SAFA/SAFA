package edu.nd.crc.safa.features.onboarding.services;

import edu.nd.crc.safa.features.onboarding.entities.app.OnboardingStateAppEntity;
import edu.nd.crc.safa.features.onboarding.entities.db.OnboardingState;
import edu.nd.crc.safa.features.onboarding.respositories.OnboardingStateRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor(onConstructor = @__({@Autowired}))
public class OnboardingService {

    private final OnboardingStateRepository stateRepository;

    /**
     * Get the onboarding state for a user
     *
     * @param user The user
     * @return The given user's onboarding state
     */
    public OnboardingState getUserState(SafaUser user) {
        return stateRepository.findByUserId(user.getUserId())
            .orElseGet(() -> stateRepository.save(new OnboardingState(user)));
    }

    /**
     * Update a given user's onboarding state from a front-end onboarding entity.
     * This will update the "completed" variable and the project ID if it is not null.
     *
     * @param user The user
     * @param stateAppEntity The updated values for the state.
     * @return The updated state
     */
    public OnboardingState updateUserStateFromAppEntity(SafaUser user, OnboardingStateAppEntity stateAppEntity) {
        OnboardingState state = getUserState(user);
        state.setCompleted(stateAppEntity.isCompleted());

        if (stateAppEntity.getProjectId() != null) {
            state.setProjectId(stateAppEntity.getProjectId());
        }

        return save(state);
    }

    /**
     * Saves an onboarding state to the database
     *
     * @param state The state to save
     * @return The saved state
     */
    public OnboardingState save(OnboardingState state) {
        return stateRepository.save(state);
    }
}

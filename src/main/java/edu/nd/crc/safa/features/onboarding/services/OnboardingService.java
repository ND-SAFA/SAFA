package edu.nd.crc.safa.features.onboarding.services;

import java.util.function.Consumer;

import edu.nd.crc.safa.features.onboarding.entities.app.OnboardingStateAppEntity;
import edu.nd.crc.safa.features.onboarding.entities.db.OnboardingState;
import edu.nd.crc.safa.features.onboarding.respositories.OnboardingStateRepository;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
    public OnboardingState getState(SafaUser user) {
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
    public OnboardingState updateStateFromAppEntity(SafaUser user, OnboardingStateAppEntity stateAppEntity) {
        return updateState(user, state -> {
            state.setCompleted(stateAppEntity.isCompleted());

            if (stateAppEntity.getProjectId() != null) {
                state.setProjectId(stateAppEntity.getProjectId());
            }
        });
    }

    /**
     * Update the project for a user's onboarding state
     *
     * @param user The user
     * @param project The new project
     * @return The updated state
     */
    public OnboardingState updateStateProject(SafaUser user, Project project) {
        return updateState(user, state -> state.setProjectId(project.getProjectId()));
    }

    /**
     * Update the completed value for a user's onboarding state
     *
     * @param user The user
     * @param completed Whether the onboarding has completed
     * @return The updated state
     */
    public OnboardingState updateStateCompleted(SafaUser user, boolean completed) {
        return updateState(user, state -> state.setCompleted(completed));
    }

    /**
     * Update a user's state and save it in the database
     *
     * @param user The user
     * @param updateFunction The function that does the updates
     * @return The updated state
     */
    private OnboardingState updateState(SafaUser user, Consumer<OnboardingState> updateFunction) {
        OnboardingState state = getState(user);
        updateFunction.accept(state);
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

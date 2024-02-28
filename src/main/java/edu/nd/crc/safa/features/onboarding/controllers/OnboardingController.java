package edu.nd.crc.safa.features.onboarding.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.onboarding.entities.app.OnboardingStateAppEntity;
import edu.nd.crc.safa.features.onboarding.services.OnboardingService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OnboardingController extends BaseController {

    private final OnboardingService onboardingService;

    @Autowired
    public OnboardingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                OnboardingService onboardingService) {
        super(resourceBuilder, serviceProvider);
        this.onboardingService = onboardingService;
    }

    /**
     * Get the onboarding state for the current user
     *
     * @return The current user's onboarding state
     */
    @GetMapping(AppRoutes.Onboarding.ROOT)
    public OnboardingStateAppEntity getUserOnboardingState() {
        SafaUser user = getCurrentUser();
        return new OnboardingStateAppEntity(onboardingService.getState(user));
    }

    /**
     * Update the user's onboarding state
     *
     * @param updatedState The updated values for the state
     * @return The updated state
     */
    @PutMapping(AppRoutes.Onboarding.ROOT)
    public OnboardingStateAppEntity updateUserOnboardingState(@RequestBody OnboardingStateAppEntity updatedState) {
        SafaUser user = getCurrentUser();
        return new OnboardingStateAppEntity(onboardingService.updateStateFromAppEntity(user, updatedState));
    }
}

package edu.nd.crc.safa.features.onboarding.respositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.onboarding.entities.db.OnboardingState;

import org.springframework.data.repository.CrudRepository;

public interface OnboardingStateRepository extends CrudRepository<OnboardingState, UUID> {
    Optional<OnboardingState> findByUserId(UUID userId);
}

package edu.nd.crc.safa.features.users.repositories;

import edu.nd.crc.safa.features.users.entities.db.UserApiKey;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository for managing UserApiKey entities.
 */
@Repository
public interface UserApiKeyRepository extends JpaRepository<UserApiKey, UUID> {

    /**
     * Find API keys by user ID.
     * @param userId The user ID to search for
     * @return Optional containing the UserApiKey if found
     */
    Optional<UserApiKey> findByUserUserId(UUID userId);

    /**
     * Delete API keys by user ID.
     * @param userId The user ID whose API keys should be deleted
     */
    void deleteByUserUserId(UUID userId);

    /**
     * Check if API keys exist for a user.
     * @param userId The user ID to check
     * @return true if API keys exist for this user
     */
    boolean existsByUserUserId(UUID userId);
}

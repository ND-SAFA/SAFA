package edu.nd.crc.safa.features.users.services;

import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.entities.db.UserApiKey;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.repositories.UserApiKeyRepository;
import edu.nd.crc.safa.security.EncryptionService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;
import java.util.UUID;

/**
 * Service for managing user API keys.
 * Handles encryption/decryption and CRUD operations for user API keys.
 */
@Service
@AllArgsConstructor
public class UserApiKeyService {

    private final EncryptionService encryptionService;
    private final UserApiKeyRepository apiKeyRepository;
    private final SafaUserRepository userRepository;

    /**
     * DTO for returning decrypted API keys.
     */
    public static class UserApiKeys {
        private final String openaiKey;
        private final String anthropicKey;
        private final String preferredProvider;

        public UserApiKeys(String openaiKey, String anthropicKey, String preferredProvider) {
            this.openaiKey = openaiKey;
            this.anthropicKey = anthropicKey;
            this.preferredProvider = preferredProvider;
        }

        public String getOpenaiKey() {
            return openaiKey;
        }

        public String getAnthropicKey() {
            return anthropicKey;
        }

        public String getPreferredProvider() {
            return preferredProvider;
        }
    }

    /**
     * Save encrypted API keys for user.
     *
     * @param userId            The user ID
     * @param openaiKey         OpenAI API key (null to skip update)
     * @param anthropicKey      Anthropic API key (null to skip update)
     * @param preferredProvider Preferred LLM provider (null to skip update)
     */
    @Transactional
    public void saveApiKeys(UUID userId, String openaiKey, String anthropicKey, String preferredProvider) {
        // Verify user exists
        SafaUser user = userRepository.findById(userId)
            .orElseThrow(() -> new SafaItemNotFoundError("User not found with ID: %s", userId));

        // Find existing API key record or create new one
        UserApiKey apiKeyEntity = apiKeyRepository.findByUserUserId(userId)
            .orElse(new UserApiKey());

        if (apiKeyEntity.getUser() == null) {
            apiKeyEntity.setUser(user);
        }

        // Update API keys (encrypt if provided)
        if (openaiKey != null && !openaiKey.trim().isEmpty()) {
            apiKeyEntity.setOpenaiApiKey(encryptionService.encrypt(openaiKey));
        }
        if (anthropicKey != null && !anthropicKey.trim().isEmpty()) {
            apiKeyEntity.setAnthropicApiKey(encryptionService.encrypt(anthropicKey));
        }

        // Update provider preference if provided
        if (preferredProvider != null && !preferredProvider.trim().isEmpty()) {
            apiKeyEntity.setPreferredProvider(preferredProvider);
        }

        apiKeyRepository.save(apiKeyEntity);
    }

    /**
     * Get decrypted API keys for user.
     *
     * @param userId The user ID
     * @return UserApiKeys containing decrypted keys (or null if not set)
     */
    @Transactional(readOnly = true)
    public UserApiKeys getApiKeys(UUID userId) {
        // Verify user exists
        if (!userRepository.existsById(userId)) {
            throw new SafaItemNotFoundError("User not found with ID: %s", userId);
        }

        // Find API keys
        Optional<UserApiKey> apiKeyEntity = apiKeyRepository.findByUserUserId(userId);

        if (apiKeyEntity.isEmpty()) {
            return new UserApiKeys(null, null, "openai");
        }

        UserApiKey keys = apiKeyEntity.get();
        return new UserApiKeys(
            keys.getOpenaiApiKey() != null ? encryptionService.decrypt(keys.getOpenaiApiKey()) : null,
            keys.getAnthropicApiKey() != null ? encryptionService.decrypt(keys.getAnthropicApiKey()) : null,
            keys.getPreferredProvider()
        );
    }

    /**
     * Delete API keys for user.
     *
     * @param userId The user ID
     */
    @Transactional
    public void deleteApiKeys(UUID userId) {
        // Verify user exists
        if (!userRepository.existsById(userId)) {
            throw new SafaItemNotFoundError("User not found with ID: %s", userId);
        }

        // Delete API keys record
        apiKeyRepository.deleteByUserUserId(userId);
    }

    /**
     * Check if user has any API keys saved.
     *
     * @param userId The user ID
     * @return true if user has at least one API key configured
     */
    @Transactional(readOnly = true)
    public boolean hasApiKeys(UUID userId) {
        return apiKeyRepository.existsByUserUserId(userId);
    }

    /**
     * Mask an API key for display purposes (shows first 4 and last 4 characters).
     *
     * @param key The API key to mask
     * @return Masked key (e.g., "sk-a...xyz") or null if key is null
     */
    public static String maskApiKey(String key) {
        if (key == null || key.length() < 8) {
            return null;
        }
        return key.substring(0, Math.min(4, key.length())) + "..." +
            key.substring(Math.max(0, key.length() - 4));
    }
}

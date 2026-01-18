package edu.nd.crc.safa.features.users.controllers;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.app.ApiKeysRequest;
import edu.nd.crc.safa.features.users.entities.app.ApiKeysResponse;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.users.services.UserApiKeyService;
import edu.nd.crc.safa.features.users.services.UserApiKeyService.UserApiKeys;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller for managing user API keys.
 * Provides endpoints for users to save, retrieve, and delete their own API keys.
 */
@RestController
@RequestMapping(AppRoutes.Accounts.API_KEYS)
@AllArgsConstructor
public class UserApiKeyController {

    private final UserApiKeyService apiKeyService;
    private final SafaUserService userService;

    /**
     * Save user's API keys.
     * Only updates keys that are provided (non-null and non-empty).
     *
     * @param request The API keys to save
     * @return Empty response with 200 OK
     */
    @PostMapping
    public ResponseEntity<Void> saveApiKeys(@RequestBody ApiKeysRequest request) {
        SafaUser currentUser = userService.getCurrentUser();

        apiKeyService.saveApiKeys(
            currentUser.getUserId(),
            request.getOpenaiApiKey(),
            request.getAnthropicApiKey(),
            request.getPreferredProvider()
        );

        return ResponseEntity.ok().build();
    }

    /**
     * Get user's API keys (returns masked version for security).
     *
     * @return ApiKeysResponse with masked API keys
     */
    @GetMapping
    public ResponseEntity<ApiKeysResponse> getApiKeys() {
        SafaUser currentUser = userService.getCurrentUser();

        UserApiKeys keys = apiKeyService.getApiKeys(currentUser.getUserId());
        boolean hasKeys = apiKeyService.hasApiKeys(currentUser.getUserId());

        // Return masked version for security
        ApiKeysResponse response = new ApiKeysResponse(
            UserApiKeyService.maskApiKey(keys.getOpenaiKey()),
            UserApiKeyService.maskApiKey(keys.getAnthropicKey()),
            keys.getPreferredProvider(),
            hasKeys
        );

        return ResponseEntity.ok(response);
    }

    /**
     * Delete user's API keys.
     *
     * @return Empty response with 204 No Content
     */
    @DeleteMapping
    public ResponseEntity<Void> deleteApiKeys() {
        SafaUser currentUser = userService.getCurrentUser();

        apiKeyService.deleteApiKeys(currentUser.getUserId());

        return ResponseEntity.noContent().build();
    }
}

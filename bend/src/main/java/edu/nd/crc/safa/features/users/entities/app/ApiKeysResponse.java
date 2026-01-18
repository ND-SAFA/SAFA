package edu.nd.crc.safa.features.users.entities.app;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for retrieving user API keys (masked for security).
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApiKeysResponse {
    /**
     * Masked OpenAI API key (e.g., "sk-a...xyz") or null if not set.
     */
    private String openaiApiKey;

    /**
     * Masked Anthropic API key (e.g., "sk-ant-...xyz") or null if not set.
     */
    private String anthropicApiKey;

    /**
     * The user's preferred LLM provider (openai or anthropic).
     */
    private String preferredProvider;

    /**
     * Whether the user has any API keys configured.
     */
    private boolean hasKeys;
}

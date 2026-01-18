package edu.nd.crc.safa.features.users.entities.app;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for saving user API keys.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApiKeysRequest {
    /**
     * OpenAI API key (null or empty to skip update).
     */
    private String openaiApiKey;

    /**
     * Anthropic API key (null or empty to skip update).
     */
    private String anthropicApiKey;

    /**
     * Preferred LLM provider (openai or anthropic).
     */
    private String preferredProvider;
}

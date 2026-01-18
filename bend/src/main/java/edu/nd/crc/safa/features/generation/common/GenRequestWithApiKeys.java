package edu.nd.crc.safa.features.generation.common;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

/**
 * Base class for gen-api requests that includes user-specific API keys.
 * Subclasses can inherit these fields to automatically include API keys in requests.
 */
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public abstract class GenRequestWithApiKeys {
    /**
     * OpenAI API key for this request (optional, falls back to environment if not provided).
     */
    private String openaiApiKey;

    /**
     * Anthropic API key for this request (optional, falls back to environment if not provided).
     */
    private String anthropicApiKey;
}

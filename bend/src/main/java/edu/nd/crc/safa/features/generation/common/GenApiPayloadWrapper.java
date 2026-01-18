package edu.nd.crc.safa.features.generation.common;

import com.fasterxml.jackson.annotation.JsonUnwrapped;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

/**
 * Wrapper for gen-api requests that adds user-specific API keys to any payload.
 * This allows injecting API keys without modifying existing request classes.
 *
 * @param <T> The type of the wrapped payload
 */
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenApiPayloadWrapper<T> {
    /**
     * The original request payload (unwrapped into the parent object during serialization).
     */
    @JsonUnwrapped
    private T payload;

    /**
     * OpenAI API key for this request (optional, falls back to environment if not provided).
     */
    private String openaiApiKey;

    /**
     * Anthropic API key for this request (optional, falls back to environment if not provided).
     */
    private String anthropicApiKey;

    /**
     * Preferred LLM provider for this request (openai or anthropic).
     */
    private String preferredProvider;

    public GenApiPayloadWrapper(T payload, String openaiApiKey, String anthropicApiKey, String preferredProvider) {
        this.payload = payload;
        this.openaiApiKey = openaiApiKey;
        this.anthropicApiKey = anthropicApiKey;
        this.preferredProvider = preferredProvider;
    }
}

package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

/**
 * Gen response to chat request.
 */
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class GenChatResponse {
    /**
     * The message the AI responded with.
     */
    private String message;
    /**
     * The artifact IDs used to cite
     */
    private List<String> artifactIds = new ArrayList<>();
}

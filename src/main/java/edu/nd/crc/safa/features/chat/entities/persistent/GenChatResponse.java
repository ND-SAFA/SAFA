package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

/**
 * Gen response to chat request.
 */
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenChatResponse {
    /**
     * The message the AI responded with.
     */
    private String response;
    /**
     * The artifact IDs used to cite
     */
    private List<GenerationArtifact> relatedArtifacts = new ArrayList<>();
}

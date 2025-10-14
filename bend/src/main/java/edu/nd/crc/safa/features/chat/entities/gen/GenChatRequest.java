package edu.nd.crc.safa.features.chat.entities.gen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenChatRequest {
    /**
     * The dataset used in context.
     */
    private GenerationDataset dataset;
    /**
     * The chat history.
     */
    private List<GenChatMessage> chatHistory;
}

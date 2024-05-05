package edu.nd.crc.safa.features.chat.entities.dtos;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class SendChatMessageRequest {
    /**
     * Artifact Ids being asked about.
     */
    private List<UUID> artifactIds = new ArrayList<>();

    /**
     * The user message in chat.
     */
    @NotNull
    private String message;
}

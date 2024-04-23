package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.List;
import java.util.UUID;

import lombok.Data;

@Data
public class GenChatResponse {
    private String message;
    private List<UUID> artifactIds;
}

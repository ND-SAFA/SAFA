package edu.nd.crc.safa.test.features.chat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;
import edu.nd.crc.safa.test.services.builders.RootBuilder;

import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Data
public class ChatTestData {
    public static final String artifactBody = "artifact body";
    public static final String artifactType = "artifact type";
    public static final String userMessageText = "this is the user message.";
    public static final String artifactName = "RE-8";
    public static final String responseText = "Response";
    public static final String chatTitle = "Hello";

    private ProjectVersion projectVersion;
    private List<String> artifactNames;
    private List<UUID> artifactIds;
    private ArtifactAppEntity artifact;

    public static ArtifactAppEntity getArtifactAppEntity() {
        ArtifactAppEntity artifact = new ArtifactAppEntity();
        artifact.setBody(artifactBody);
        artifact.setType(artifactType);
        artifact.setName(artifactName);
        return artifact;
    }

    public static ChatDTO retrieveChat(UUID chatId) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Chat.Message.MESSAGE_GET)
            .withCustomReplacement("chatId", chatId)
            .getAsType(ChatDTO.class);
    }

    public void createProject(RootBuilder rootBuilder, ProjectVersion projectVersion) {
        this.artifact = ChatTestData.getArtifactAppEntity();
        ArtifactAppEntity artifactAdded = rootBuilder.actions(a -> a.commit(
                CommitBuilder
                    .withVersion(projectVersion)
                    .withAddedArtifact(this.artifact)
            ).getArtifact(ModificationType.ADDED, 0))
            .get();
        this.artifactNames = List.of(artifactAdded.getName());
        this.artifactIds = List.of(artifactAdded.getId());
    }
}

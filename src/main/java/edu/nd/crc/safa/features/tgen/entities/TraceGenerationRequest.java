package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate trace links between artifacts.
 */
@Data
@NoArgsConstructor
public class TraceGenerationRequest {
    /**
     * List of source artifacts.
     */
    @NotNull
    List<ArtifactAppEntity> sourceArtifacts;
    /**
     * List of target artifacts.
     */
    @NotNull
    List<ArtifactAppEntity> targetArtifacts;
    /**
     * The method to generate trace links with.
     */
    TraceGenerationMethod method = TraceGenerationMethod.getDefault();
    /**
     * The project version to commit them too.
     */
    ProjectVersion projectVersion = new ProjectVersion();

    @JsonIgnore
    public int size() {
        return this.sourceArtifacts.size() * this.targetArtifacts.size();
    }
}

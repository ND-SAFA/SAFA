package edu.nd.crc.safa.features.models.tgen.entities;

import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotEmpty;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate trace links between artifacts.
 */
@NoArgsConstructor
@Data
public class TraceGenerationRequest {
    /**
     * The artifact levels being traced against.
     */
    @NotEmpty
    List<TracingRequest> requests = new ArrayList<>();

    /**
     * The project version to commit them too.
     */
    ProjectVersion projectVersion = new ProjectVersion();

    @JsonIgnore
    public int size() {
        return this.getRequests().size();
    }

    public void addTracingRequest(BaseGenerationModels method,
                                  ModelAppEntity model,
                                  String source,
                                  String target) {
        ArtifactLevelRequest artifactLevelRequest = new ArtifactLevelRequest(source, target);
        TracingRequest tracingRequest = new TracingRequest(
            method,
            model,
            new ArrayList<>(List.of(artifactLevelRequest))
        );
        this.requests.add(tracingRequest);
    }
}

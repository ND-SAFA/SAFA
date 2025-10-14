package edu.nd.crc.safa.features.generation.tgen.entities;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate trace links between artifacts.
 */
@NoArgsConstructor
@Data
public class TGenRequestAppEntity {
    /**
     * The artifact levels being traced against.
     */
    @NotEmpty
    private List<TracingRequest> requests = new ArrayList<>();

    /**
     * The project version to commit them too.
     */
    private ProjectVersion projectVersion = new ProjectVersion();

    /**
     * @return Returns the number of artifact levels being traced.
     */
    @JsonIgnore
    public int size() {
        return this.getRequests().size();
    }

    /**
     * Adds tracing request between child and parent artifact types.
     *
     * @param childType  Name of child artifact type.
     * @param parentType Name of parent artifact type.
     */
    public void addTracingRequest(String childType,
                                  String parentType) {
        addTracingRequest(childType, parentType, TGenAlgorithms.getDefaultAlgorithm());
    }

    /**
     * Adds tracing request between child and parent artifact types.
     *
     * @param childType        Name of child artifact type.
     * @param parentType       Name of parent artifact type.
     * @param generationMethod The generational method.
     */
    public void addTracingRequest(String childType,
                                  String parentType,
                                  TGenAlgorithms generationMethod) {
        ArtifactLevelRequest artifactLevelRequest = new ArtifactLevelRequest(childType, parentType);
        TracingRequest tracingRequest = new TracingRequest(
            new ArrayList<>(List.of(artifactLevelRequest)),
            generationMethod
        );
        this.requests.add(tracingRequest);
    }
}

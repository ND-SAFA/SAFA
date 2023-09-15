package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A request to summarize artifacts from the front-end.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SummarizeArtifactRequestDTO {
    /**
     * The artifacts to summarize and their type.
     */
    @NotEmpty
    private List<@NotNull UUID> artifacts;
    /**
     * The version of the artifacts to summarize.
     */
    @Nullable
    private ProjectVersion projectVersion;
    /**
     * The project summary.
     */
    @Nullable
    private String projectSummary;

    public void setProjectSummary(String projectSummary) {
        this.projectSummary = projectSummary == null || projectSummary.isEmpty() ? null : projectSummary;
    }
}

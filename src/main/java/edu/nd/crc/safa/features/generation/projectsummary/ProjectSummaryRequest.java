package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class ProjectSummaryRequest {
    /**
     * The artifacts in the project to summarize project with.
     */
    List<GenerationArtifact> artifacts;
}

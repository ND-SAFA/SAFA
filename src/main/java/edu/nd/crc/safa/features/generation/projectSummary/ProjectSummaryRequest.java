package edu.nd.crc.safa.features.generation.projectSummary;

import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class ProjectSummaryRequest {
    /**
     * The artifacts in the project to summarize project with.
     */
    Map<String, String> artifacts;
}

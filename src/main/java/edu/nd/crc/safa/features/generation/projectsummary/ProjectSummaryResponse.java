package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@JsonIgnoreProperties(ignoreUnknown = true)
@Data
public class ProjectSummaryResponse implements ITGenResponse {
    /**
     * The project summary / specification.
     */
    private String summary;
    /**
     * List of summarized artifacts.
     */
    private List<GenerationArtifact> artifacts;
    /**
     * The logs associated with job.
     */
    private List<String> logs;
}

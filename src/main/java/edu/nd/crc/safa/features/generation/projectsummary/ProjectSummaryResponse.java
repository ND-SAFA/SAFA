package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import lombok.Data;

@Data
public class ProjectSummaryResponse implements ITGenResponse {
    /**
     * The project summary / specification.
     */
    String summary;
    /**
     * The logs associated with job.
     */
    List<String> logs;
}

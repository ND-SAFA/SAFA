package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@JsonIgnoreProperties(ignoreUnknown = true)
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

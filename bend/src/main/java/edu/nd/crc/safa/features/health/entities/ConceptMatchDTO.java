package edu.nd.crc.safa.features.health.entities;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class ConceptMatchDTO {
    /**
     * The artifact ID containing concept ID
     */
    private String artifactId;
    /**
     * ID of concept artifact matched.
     */
    private String conceptId;
    /**
     * Index of start of match string.
     */
    private int startLoc;
    /**
     * Index of end of match string.
     */
    private int endLoc;

    /**
     * @return Constructs manual trace link to direct concept match.
     */
    public TraceAppEntity toTrace() {
        TraceAppEntity trace = new TraceAppEntity();
        trace.setTargetName(this.conceptId);
        trace.setSourceName(this.artifactId);
        trace.asManualTrace();
        return trace;
    }
}

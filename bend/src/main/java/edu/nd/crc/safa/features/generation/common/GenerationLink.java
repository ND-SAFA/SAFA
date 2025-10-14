package edu.nd.crc.safa.features.generation.common;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A predicted trace link.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@NoArgsConstructor
public class GenerationLink {
    /**
     * The child name;
     */
    private String source;
    /**
     * The parent name.
     */
    private String target;
    /**
     * The similarity score.
     */
    private double score;
    /**
     * The true label between them.
     */
    private double label = -1;
    /**
     * The trace explanation.
     */
    private String explanation;

    public GenerationLink(TraceAppEntity trace) {
        this.source = trace.getSourceName();
        this.target = trace.getTargetName();
        this.score = trace.getScore();
        this.explanation = trace.getExplanation();
        this.label = trace.getTraceType() == TraceType.MANUAL ? 1 : -1;
    }

    /**
     * @return trace app entity with link information.
     */
    public TraceAppEntity toTrace() {
        TraceAppEntity trace = new TraceAppEntity();
        trace.setSourceName(this.source);
        trace.setTargetName(this.target);
        if (this.label == 1) {
            trace.asManualTrace();
        } else {
            trace.asGeneratedTrace(this.score);
        }
        trace.setExplanation(this.explanation);
        return trace;
    }
}

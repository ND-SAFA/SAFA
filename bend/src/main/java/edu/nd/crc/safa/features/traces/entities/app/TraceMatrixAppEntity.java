package edu.nd.crc.safa.features.traces.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;

import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Data
public class TraceMatrixAppEntity implements IAppEntity {

    /**
     * ID of this trace matrix entity in the database
     */
    private UUID id;

    /**
     * Name of the source type
     */
    private String sourceType;

    /**
     * Name of the target type
     */
    private String targetType;

    /**
     * Number of links between the source type and the target type in the current project version
     */
    private int count;

    /**
     * Number of links between the source and target types that are marked as generated
     */
    private int generatedCount;

    /**
     * Number of links between the source and target types that are marked as generated and are approved
     */
    private int approvedCount;

    public TraceMatrixAppEntity(TraceMatrixEntry traceMatrixEntry) {
        this.id = traceMatrixEntry.getId();
        this.sourceType = traceMatrixEntry.getSourceType().getName();
        this.targetType = traceMatrixEntry.getTargetType().getName();
        this.count = traceMatrixEntry.getCount();
        this.generatedCount = traceMatrixEntry.getGeneratedCount();
        this.approvedCount = traceMatrixEntry.getApprovedCount();
    }
}

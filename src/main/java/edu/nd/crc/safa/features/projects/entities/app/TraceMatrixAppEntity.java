package edu.nd.crc.safa.features.projects.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;

import lombok.Data;

@Data
public class TraceMatrixAppEntity implements IAppEntity {
    private UUID id;
    private String sourceType;
    private String targetType;
    private int count;
    private int generatedCount;
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

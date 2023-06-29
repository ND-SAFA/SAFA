package edu.nd.crc.safa.features.projects.entities.app;

import java.util.UUID;

import lombok.Data;

@Data
public class TraceMatrixAppEntity {
    private UUID id = UUID.randomUUID();
    private String sourceType;
    private String targetType;
    private int count;
    private int generatedCount;
    private int approvedCount;
}

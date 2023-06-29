package edu.nd.crc.safa.features.projects.graph;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.projects.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import org.javatuples.Pair;

public class TimCalculator {

    /**
     * Get trace matrix info for a project
     *
     * @param entities The entities in the project
     * @return Trace matrix info indicating what types trace to what other types
     */
    public static List<TraceMatrixAppEntity> getTimInfo(ProjectEntities entities) {
        TimGenerationDataStructures data = new TimGenerationDataStructures();
        handleArtifacts(data, entities.getArtifacts());
        handleTraces(data, entities.getTraces());
        return List.copyOf(data.timTraces.values());
    }

    /**
     * For each trace, get the source and target type, and update trace matrix info to reflect
     * that this trace connects these types.
     *
     * @param data The data objects we need for our calculations
     * @param traces The list of traces in the project
     */
    private static void handleTraces(TimGenerationDataStructures data, List<TraceAppEntity> traces) {
        for (TraceAppEntity trace : traces) {
            ArtifactAppEntity sourceArtifact = data.uuidToArtifact.get(trace.getSourceId());
            ArtifactAppEntity targetArtifact = data.uuidToArtifact.get(trace.getTargetId());
            String sourceType = sourceArtifact.getType();
            String targetType = targetArtifact.getType();

            Pair<String, String> typePair = new Pair<>(sourceType, targetType);
            ensureDefaultTraceEntity(data, typePair);
            TraceMatrixAppEntity timTrace = data.timTraces.get(typePair);
            updateLinkCounts(trace, timTrace);
        }
    }

    /**
     * For each artifact, add it to our UUID -> artifact map
     *
     * @param data The data objects we need for our calculations
     * @param artifacts The list of artifacts in the project
     */
    private static void handleArtifacts(TimGenerationDataStructures data, List<ArtifactAppEntity> artifacts) {
        for (ArtifactAppEntity artifact : artifacts) {
            data.uuidToArtifact.put(artifact.getId(), artifact);
        }
    }

    /**
     * Makes sure there is a trace matrix object for this pair of types.
     *
     * @param data The data objects we need for our calculations
     * @param typePair The (source,target) pair of types
     */
    private static void ensureDefaultTraceEntity(TimGenerationDataStructures data, Pair<String, String> typePair) {
        if (!data.timTraces.containsKey(typePair)) {
            TraceMatrixAppEntity timTrace = new TraceMatrixAppEntity();
            timTrace.setSourceType(typePair.getValue0());
            timTrace.setTargetType(typePair.getValue1());
            data.timTraces.put(typePair, timTrace);
        }
    }

    /**
     * Updates a trace matrix object with a particular trace, adding it to the matrix's count variables.
     *
     * @param trace The trace we're counting
     * @param timTrace The object storing the counts for the types in this trace
     */
    private static void updateLinkCounts(TraceAppEntity trace, TraceMatrixAppEntity timTrace) {
        timTrace.setCount(timTrace.getCount() + 1);
        if (trace.getTraceType() == TraceType.GENERATED) {
            timTrace.setGeneratedCount(timTrace.getGeneratedCount() + 1);
            if (trace.getApprovalStatus() == ApprovalStatus.APPROVED) {
                timTrace.setApprovedCount(timTrace.getApprovedCount() + 1);
            }
        }
    }

    private static class TimGenerationDataStructures {
        public Map<UUID, ArtifactAppEntity> uuidToArtifact = new HashMap<>();
        public Map<Pair<String, String>, TraceMatrixAppEntity> timTraces = new HashMap<>();
    }
}

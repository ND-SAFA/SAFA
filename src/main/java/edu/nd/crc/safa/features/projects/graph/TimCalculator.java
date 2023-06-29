package edu.nd.crc.safa.features.projects.graph;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.types.TypeAppEntity;

import org.javatuples.Pair;

public class TimCalculator {

    /**
     * Attach trace matrix info to a project. This will count all artifacts of a given type
     * and update the type counts, as well as calculate the trace matrix values and attach
     * them to the project.
     *
     * @param project The project to add TIM info to.
     */
    public static void attachTimInfo(ProjectAppEntity project) {
        TimGenerationDataStructures data = new TimGenerationDataStructures();
        handleTypes(data, project.getArtifactTypes());
        handleArtifacts(data, project.getArtifacts());
        handleTraces(data, project.getTraces());
        project.setTraceMatrices(List.copyOf(data.timTraces.values()));
    }

    /**
     * Puts type entities into a map to make them easier to work with.
     *
     * @param data The data objects we need for our calculations
     * @param artifactTypes The types in the project
     */
    private static void handleTypes(TimGenerationDataStructures data, List<TypeAppEntity> artifactTypes) {
        for (TypeAppEntity type : artifactTypes) {
            data.typeEntities.put(type.getName(), type);
        }
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

            if (!data.typeTraces.containsKey(sourceType)) {
                data.typeTraces.put(sourceType, new HashSet<>());
            }
            data.typeTraces.get(sourceType).add(targetType);

            Pair<String, String> typePair = new Pair<>(sourceType, targetType);
            ensureDefaultTraceEntity(data, typePair);
            TraceMatrixAppEntity timTrace = data.timTraces.get(typePair);
            updateLinkCounts(trace, timTrace);
        }
    }

    /**
     * For each artifact, update the count of this artifact's type
     *
     * @param data The data objects we need for our calculations
     * @param artifacts The list of artifacts in the project
     */
    private static void handleArtifacts(TimGenerationDataStructures data, List<ArtifactAppEntity> artifacts) {
        for (ArtifactAppEntity artifact : artifacts) {
            data.uuidToArtifact.put(artifact.getId(), artifact);
            String type = artifact.getType();
            TypeAppEntity typeEntity = data.typeEntities.get(type);
            typeEntity.setCount(typeEntity.getCount() + 1);
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
        public Map<String, Set<String>> typeTraces = new HashMap<>();
        public Map<String, TypeAppEntity> typeEntities = new HashMap<>();
        public Map<Pair<String, String>, TraceMatrixAppEntity> timTraces = new HashMap<>();
    }
}

package edu.nd.crc.safa.flatfiles.entities;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;

import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

/**
 * Creates mapping data structures for trace links for easy retrieval.
 */
public class TraceMaps {
    Map<String, Map<String, List<TraceAppEntity>>> type2traces;

    public TraceMaps(ProjectAppEntity projectAppEntity, ArtifactMaps artifactMaps) {
        this.type2traces = new HashMap<>();
        this.createType2Traces(projectAppEntity, artifactMaps);
    }

    private void createType2Traces(
        ProjectAppEntity projectAppEntity,
        ArtifactMaps artifactMaps
    ) {
        for (TraceAppEntity trace : projectAppEntity.traces) {
            String sourceType = artifactMaps.getArtifactByName(trace.sourceName).type;
            String targetType = artifactMaps.getArtifactByName(trace.targetName).type;

            if (type2traces.containsKey(sourceType)) {
                if (type2traces.containsKey(targetType)) {
                    type2traces.get(sourceType).get(targetType).add(trace);
                } else {
                    Map<String, List<TraceAppEntity>> sourceTypeTraces = type2traces.get(sourceType);
                    sourceTypeTraces.put(targetType, new ArrayList<>(List.of(trace)));
                }
            } else {
                Map<String, List<TraceAppEntity>> sourceTypeTraces = new Hashtable<>();
                sourceTypeTraces.put(targetType, new ArrayList<>(List.of(trace)));
                type2traces.put(sourceType, sourceTypeTraces);
            }
        }
    }

    public Set<String> getSourceTypes() {
        return this.type2traces.keySet();
    }

    public Set<String> getTargetTypes(String sourceType) {
        return this.type2traces.get(sourceType).keySet();
    }

    public List<TraceAppEntity> getTracesBetweenTypes(String sourceType, String targetType) {
        return this.type2traces.get(sourceType).get(targetType);
    }
}

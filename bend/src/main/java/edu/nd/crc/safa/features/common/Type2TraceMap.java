package edu.nd.crc.safa.features.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

/**
 * Creates mapping between source type to target type to trace links between those two.
 */
public class Type2TraceMap {
    private Map<String, Map<String, List<TraceAppEntity>>> type2traces;

    public Type2TraceMap(ProjectAppEntity projectAppEntity, ProjectEntities projectEntityMaps) {
        this.type2traces = new HashMap<>();
        this.createType2Traces(projectAppEntity, projectEntityMaps);
    }

    private void createType2Traces(
        ProjectAppEntity projectAppEntity,
        ProjectEntities projectEntityMaps
    ) {
        for (TraceAppEntity trace : projectAppEntity.getTraces()) {
            String sourceType = projectEntityMaps.getArtifactByName(trace.getSourceName()).getType();
            String targetType = projectEntityMaps.getArtifactByName(trace.getTargetName()).getType();

            if (type2traces.containsKey(sourceType)) {
                Map<String, List<TraceAppEntity>> sourceTypeTraces = type2traces.get(sourceType);
                if (sourceTypeTraces.containsKey(targetType)) {
                    type2traces.get(sourceType).get(targetType).add(trace);
                } else {
                    sourceTypeTraces.put(targetType, new ArrayList<>(List.of(trace)));
                }
            } else {
                Map<String, List<TraceAppEntity>> sourceTypeTraces = new HashMap<>();
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

package edu.nd.crc.safa.features.flatfiles.parser.base;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.flatfiles.parser.interfaces.ITraceFile;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains trace file constants and validation
 */
public abstract class AbstractTraceFile<I> extends AbstractDataFile<TraceAppEntity, I> implements ITraceFile {

    protected AbstractTraceFile(List<TraceAppEntity> entities) {
        super(entities);
    }

    protected AbstractTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractTraceFile(MultipartFile file) throws IOException {
        super(file, true);
    }

    @Override
    public Pair<List<TraceAppEntity>, List<String>> validateInProject(ProjectAppEntity projectAppEntity) {
        // Step - Create map of artifact names
        List<String> projectArtifactNames = projectAppEntity.getArtifactNames();
        List<String> errors = new ArrayList<>();
        List<TraceAppEntity> validTraces = new ArrayList<>();
        for (TraceAppEntity entity : this.getEntities()) {
            List<String> traceAppEntityErrors = assertTraceContainsPointers(entity, projectArtifactNames);
            if (traceAppEntityErrors.isEmpty()) {
                validTraces.add(entity);
            } else {
                errors.addAll(traceAppEntityErrors);
            }
        }
        return new Pair<>(validTraces, errors);
    }

    @Override
    public Pair<List<TraceAppEntity>, List<String>> validateEntitiesCreated() {
        return filterDuplicates(this.getEntities(), new ArrayList<>());
    }

    private Pair<List<TraceAppEntity>, List<String>> filterDuplicates(List<TraceAppEntity> traces,
                                                                      List<String> errors) {
        Map<String, List<String>> source2target = new HashMap<>();
        List<TraceAppEntity> validTraces = new ArrayList<>();
        for (TraceAppEntity trace : traces) {
            String sourceName = trace.getSourceName();
            String targetName = trace.getTargetName();
            if (source2target.containsKey(sourceName)) {
                List<String> targets = source2target.get(sourceName);
                if (targets.contains(targetName)) {
                    String error = String.format("Duplicate trace link found: %s", trace);
                    errors.add(error);
                    continue;
                } else {
                    targets.add(targetName);
                }
            } else {
                source2target.put(sourceName, new ArrayList<>());
            }
            validTraces.add(trace);
        }

        return new Pair<>(validTraces, errors);
    }

    private List<String> assertTraceContainsPointers(TraceAppEntity traceAppEntity, List<String> artifactNames) {
        List<String> errors = new ArrayList<>();
        if (!artifactNames.contains(traceAppEntity.getSourceName())) {
            errors.add("Link contains unknown source artifact:" + traceAppEntity.getSourceName());
        }
        if (!artifactNames.contains(traceAppEntity.getTargetName())) {
            errors.add("Link contains unknown target artifact:" + traceAppEntity.getTargetName());
        }
        return errors;
    }
}

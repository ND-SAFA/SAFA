package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains trace file constants and validation
 */
public abstract class AbstractTraceFile<I> extends AbstractDataFile<TraceAppEntity, I> {

    protected AbstractTraceFile(List<TraceAppEntity> entities) {
        super(entities);
    }

    protected AbstractTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractTraceFile(MultipartFile file) throws IOException {
        super(file, true);
    }

    public static void validateTraceDefinition(JSONObject traceDefinition) {
        FileUtilities.assertHasKeys(traceDefinition, Constants.REQUIRED_DEFINITION_FIELDS);
        List<String> oneRequired = List.of(Constants.GENERATE_LINKS_PARAM, FlatFileParser.Constants.FILE_PARAM);
        boolean containsOne = false;
        for (String oneRequiredField : oneRequired) {
            if (traceDefinition.has(oneRequiredField)) {
                containsOne = true;
            }
        }
        if (!containsOne) {
            throw new SafaError("Definition missing one of required fields:" + oneRequired);
        }
    }

    @Override
    public Pair<List<TraceAppEntity>, List<String>> validateInProject(ProjectAppEntity projectAppEntity) {
        // Step - Create map of artifact names
        List<String> projectArtifactNames = projectAppEntity.getArtifactNames();
        List<String> errors = new ArrayList<>();
        List<TraceAppEntity> validTraces = new ArrayList<>();
        for (TraceAppEntity entity : this.entities) {
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
        return filterDuplicates(this.entities, new ArrayList<>());
    }

    private Pair<List<TraceAppEntity>, List<String>> filterDuplicates(List<TraceAppEntity> traces,
                                                                      List<String> errors) {
        Map<String, List<String>> source2target = new HashMap<>();
        List<TraceAppEntity> validTraces = new ArrayList<>();
        for (TraceAppEntity trace : traces) {
            String sourceName = trace.sourceName;
            String targetName = trace.targetName;
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
        if (!artifactNames.contains(traceAppEntity.sourceName)) {
            errors.add("Link contains unknown source artifact:" + traceAppEntity.sourceName);
        }
        if (!artifactNames.contains(traceAppEntity.targetName)) {
            errors.add("Link contains unknown target artifact:" + traceAppEntity.sourceName);
        }
        return errors;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String GENERATE_LINKS_PARAM = "generatelinks";
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final List<String> REQUIRED_DEFINITION_FIELDS = List.of(SOURCE_PARAM, TARGET_PARAM);
    }
}

package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains trace file constants and validation
 */
public abstract class AbstractTraceFile<T> extends AbstractDataFile<TraceAppEntity, T> {
    protected AbstractTraceFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractTraceFile(MultipartFile file) throws IOException {
        super(file);
    }

    public static void validateTraceDefinition(JSONObject traceDefinition) {
        FileUtilities.assertHasKeys(traceDefinition, Constants.REQUIRED_DEFINITION_FIELDS);
        List<String> oneRequired = List.of(Constants.GENERATE_LINKS_PARAM, TimParser.Constants.FILE_PARAM);
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
    public List<String> validate(List<TraceAppEntity> entities, ProjectCommit projectCommit) {
        return null;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String GENERATE_LINKS_PARAM = "generatelinks";
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final List<String> REQUIRED_DEFINITION_FIELDS = List.of(SOURCE_PARAM, TARGET_PARAM);
    }
}

package edu.nd.crc.safa.flatFiles.entities;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

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

    @Override
    public List<String> validate(List<TraceAppEntity> entities, ProjectCommit projectCommit) {
        return null;
    }

    public static class Constants {
        public static final String GENERATE_LINKS_PARAM = "generatelinks";
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final String[] REQUIRED_COLUMNS = {SOURCE_PARAM, TARGET_PARAM};
        protected static final String[] TIM_REQUIRED_KEYS = {SOURCE_PARAM, TARGET_PARAM,
            TimParser.Constants.FILE_PARAM};

        private Constants() {
        }
    }
}

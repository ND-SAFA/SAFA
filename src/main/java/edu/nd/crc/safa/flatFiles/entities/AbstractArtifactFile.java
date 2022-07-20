package edu.nd.crc.safa.flatFiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

import org.springframework.web.multipart.MultipartFile;

/**
 * Contains artifact file constants and validation.
 */
public abstract class AbstractArtifactFile<T> extends AbstractDataFile<ArtifactAppEntity, T> {
    protected AbstractArtifactFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractArtifactFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    public List<String> validate(List<ArtifactAppEntity> newEntities, ProjectCommit projectCommit) {
        List<ArtifactAppEntity> existingEntities = projectCommit.getArtifacts().getAdded();
        List<String> existingEntityNames = existingEntities.stream().map(ArtifactAppEntity::getName).collect(Collectors.toList());
        List<String> errors = new ArrayList<>();

        for (ArtifactAppEntity artifact : existingEntities) {
            if (existingEntityNames.contains(artifact.name)) {
                errors.add("Duplicate artifact found:" + artifact.name);
            }
        }
        return errors;
    }

    public static class Constants {
        public static final String[] REQUIRED_KEYS = {TimParser.Constants.FILE_PARAM};
        public static final String NAME_PARAM = "id";
        public static final String SUMMARY_PARAM = "summary";
        public static final String CONTENT_PARAM = "content";
        public static final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};

        private Constants() {
        }
    }
}

package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains artifact file constants and validation.
 */
@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public abstract class AbstractArtifactFile<T> extends AbstractDataFile<ArtifactAppEntity, T> {
    protected AbstractArtifactFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractArtifactFile(MultipartFile file) throws IOException {
        super(file);
    }

    public static void validateArtifactDefinition(JSONObject artifactDefinition) {
        FileUtilities.assertHasKeys(artifactDefinition, Constants.REQUIRED_KEYS);
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

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final List<String> REQUIRED_KEYS = List.of(TimParser.Constants.FILE_PARAM);
    }
}

package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
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
    public List<String> validate(List<ArtifactAppEntity> newEntities, ProjectAppEntity projectAppEntity) {
        HashMap<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        List<String> errors = new ArrayList<>();

        for (ArtifactAppEntity artifact : newEntities) {
            if (name2artifact.containsKey(artifact.name)) {
                errors.add("Duplicate artifact artifact found:" + artifact.name);
            } else {
                name2artifact.put(artifact.name, artifact);
            }
        }
        return errors;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final List<String> REQUIRED_KEYS = List.of(TimParser.Constants.FILE_PARAM);
    }
}

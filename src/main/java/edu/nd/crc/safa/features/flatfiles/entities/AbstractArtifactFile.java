package edu.nd.crc.safa.features.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains artifact file constants and validation.
 */
public abstract class AbstractArtifactFile<I> extends AbstractDataFile<ArtifactAppEntity, I> {

    protected AbstractArtifactFile(List<ArtifactAppEntity> artifacts) {
        super(artifacts);
    }

    protected AbstractArtifactFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    protected AbstractArtifactFile(String pathToFile, boolean parseOnConstruct) throws IOException {
        super(pathToFile, parseOnConstruct);
    }

    protected AbstractArtifactFile(MultipartFile file) throws IOException {
        super(file, true);
    }

    protected AbstractArtifactFile(MultipartFile file, boolean parseOnConstruct) throws IOException {
        super(file, parseOnConstruct);
    }

    public static void validateArtifactDefinition(JSONObject artifactDefinition) {
        FileUtilities.assertHasKeys(artifactDefinition, Constants.REQUIRED_KEYS);
    }

    @Override
    public Pair<List<ArtifactAppEntity>, List<String>> validateInProject(ProjectAppEntity projectAppEntity) {
        HashMap<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        for (ArtifactAppEntity artifact : projectAppEntity.getArtifacts()) {
            name2artifact.put(artifact.name, artifact);
        }
        return checkForDuplicates(name2artifact);
    }

    @Override
    public Pair<List<ArtifactAppEntity>, List<String>> validateEntitiesCreated() {
        HashMap<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        return checkForDuplicates(name2artifact);
    }

    private Pair<List<ArtifactAppEntity>, List<String>> checkForDuplicates(
        HashMap<String, ArtifactAppEntity> artifactsProcessed) {
        List<String> errors = new ArrayList<>();
        List<ArtifactAppEntity> validArtifacts = new ArrayList<>();
        entities.forEach(artifact -> {
            if (artifactsProcessed.containsKey(artifact.name)) {
                String errorMessage = String.format("Duplicate artifact artifact found: %s", artifact.name);
                errors.add(errorMessage);
            } else {
                artifactsProcessed.put(artifact.name, artifact);
                validArtifacts.add(artifact);
            }
        });
        return new Pair<>(validArtifacts, errors);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final List<String> REQUIRED_KEYS = List.of(FlatFileParser.Constants.FILE_PARAM);
    }
}

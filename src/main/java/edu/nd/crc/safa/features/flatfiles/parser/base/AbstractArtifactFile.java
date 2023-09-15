package edu.nd.crc.safa.features.flatfiles.parser.base;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IArtifactFile;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * Contains artifact file constants and validation.
 */
public abstract class AbstractArtifactFile<I> extends AbstractDataFile<ArtifactAppEntity, I> implements IArtifactFile {

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

    @Override
    public Pair<List<ArtifactAppEntity>, List<String>> validateInProject(ProjectAppEntity projectAppEntity) {
        HashMap<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        for (ArtifactAppEntity artifact : projectAppEntity.getArtifacts()) {
            name2artifact.put(artifact.getName(), artifact);
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
        getEntities().forEach(artifact -> {
            if (artifactsProcessed.containsKey(artifact.getName())) {
                String errorMessage = String.format("Duplicate artifact found: %s", artifact.getName());
                errors.add(errorMessage);
            } else {
                artifactsProcessed.put(artifact.getName(), artifact);
                validArtifacts.add(artifact);
            }
        });
        return new Pair<>(validArtifacts, errors);
    }
}

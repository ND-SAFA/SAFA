package edu.nd.crc.safa.features.types;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for retrieving {@link TypeAppEntity}.
 */
@AllArgsConstructor
@Service
public class TypeService implements IAppEntityService<TypeAppEntity> {
    ArtifactTypeRepository artifactTypeRepository;

    @Override
    public List<TypeAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return getAppEntities(projectVersion.getProject());
    }

    public List<TypeAppEntity> getAppEntities(Project project) {
        return artifactTypeRepository
            .findByProject(project)
            .stream()
            .map(TypeAppEntity::new)
            .collect(Collectors.toList());
    }

    public List<TypeAppEntity> getAppEntitiesWithCounts(Project project, List<ArtifactAppEntity> artifacts) {
        List<TypeAppEntity> types = getAppEntities(project);
        addCounts(types, artifacts);
        return types;
    }

    public List<TypeAppEntity> getAppEntitiesWithCounts(ProjectVersion projectVersion, SafaUser user,
                                                        List<ArtifactAppEntity> artifacts) {
        List<TypeAppEntity> types = getAppEntities(projectVersion, user);
        addCounts(types, artifacts);
        return types;
    }

    private void addCounts(List<TypeAppEntity> types, List<ArtifactAppEntity> artifacts) {
        Map<String, TypeAppEntity> typeEntities = new HashMap<>();
        for (TypeAppEntity type : types) {
            typeEntities.put(type.getName(), type);
        }

        for (ArtifactAppEntity artifact : artifacts) {
            String type = artifact.getType();
            TypeAppEntity typeEntity = typeEntities.get(type);
            typeEntity.setCount(typeEntity.getCount() + 1);
        }
    }

    /**
     * Get the artifact type by its id.
     *
     * @param artifactTypeId the id of the artifact type
     * @return the artifact type, or null if it was not found
     */
    public ArtifactType getArtifactType(UUID artifactTypeId) {
        return artifactTypeRepository.findById(artifactTypeId).orElse(null);
    }

    /**
     * Get and artifact type for a given project by its name.
     *
     * @param project the project the type belongs to
     * @param artifactTypeName the name of the artifact type
     * @return the artifact type, or null if it was not found
     */
    public ArtifactType getArtifactType(Project project, String artifactTypeName) {
        return artifactTypeRepository.findByProjectAndNameIgnoreCase(project, artifactTypeName).orElse(null);
    }

    /**
     * Save an artifact type.
     *
     * @param artifactType the artifact type to save
     * @return the saved artifact type
     */
    public ArtifactType saveArtifactType(ArtifactType artifactType) {
        return artifactTypeRepository.save(artifactType);
    }

    /**
     * Create an artifact type for a given project.
     *
     * @param project the project the type belongs to
     * @param name the name of the artifact type
     * @return the created artifact type
     */
    public ArtifactType createArtifactType(Project project, String name) {
        ArtifactType artifactType = new ArtifactType(project, name);
        return saveArtifactType(artifactType);
    }
}

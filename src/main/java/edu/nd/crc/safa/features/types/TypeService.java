package edu.nd.crc.safa.features.types;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
    public List<TypeAppEntity> getAppEntities(ProjectVersion projectVersion) {
        return getAppEntities(projectVersion.getProject());
    }

    public List<TypeAppEntity> getAppEntities(Project project) {
        return artifactTypeRepository
            .findByProject(project)
            .stream()
            .map(TypeAppEntity::new)
            .collect(Collectors.toList());
    }
}

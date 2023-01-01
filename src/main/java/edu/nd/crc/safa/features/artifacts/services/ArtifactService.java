package edu.nd.crc.safa.features.artifacts.services;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ArtifactService implements IAppEntityService<ArtifactAppEntity> {
    ArtifactVersionRepository artifactVersionRepository;

    @Override
    public List<ArtifactAppEntity> getAppEntities(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        return versionToAppEntity(artifactVersions);
    }

    public List<ArtifactAppEntity> getAppEntities(Project project) {
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository.findByProjectVersionProject(project);
        return versionToAppEntity(artifactVersions);
    }

    private List<ArtifactAppEntity> versionToAppEntity(List<ArtifactVersion> artifactVersions) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (ArtifactVersion artifactVersion : artifactVersions) {
            ArtifactAppEntity artifactAppEntity = this.artifactVersionRepository
                .retrieveAppEntityFromVersionEntity(artifactVersion);
            artifacts.add(artifactAppEntity);
        }
        return artifacts;
    }
}

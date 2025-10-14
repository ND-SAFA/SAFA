package edu.nd.crc.safa.features.types.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.types.repositories.ArtifactTypeCountRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ArtifactTypeCountService {
    private ArtifactTypeCountRepository repo;

    public List<ArtifactTypeCount> getByProjectVersion(ProjectVersion projectVersion) {
        return repo.getByProjectVersion(projectVersion);
    }

    public List<ArtifactTypeCount> getByType(ArtifactType type) {
        return repo.getByType(type);
    }

    public Optional<ArtifactTypeCount> getByProjectVersionAndType(ProjectVersion projectVersion, ArtifactType type) {
        return repo.getByProjectVersionAndType(projectVersion, type);
    }

    public ArtifactTypeCount getOrCreate(ProjectVersion version, ArtifactType type) {
        return getByProjectVersionAndType(version, type).orElse(new ArtifactTypeCount(version, type));
    }

    public void save(ArtifactTypeCount artifactTypeCount) {
        repo.save(artifactTypeCount);
    }
}

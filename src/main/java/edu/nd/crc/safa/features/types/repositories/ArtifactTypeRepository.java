package edu.nd.crc.safa.features.types.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.utilities.GeneralRepository;

import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactTypeRepository extends GeneralRepository<ArtifactType, UUID> {

    Optional<ArtifactType> findByProjectAndNameIgnoreCase(Project project, String name);

    List<ArtifactType> findByProject(Project project);

    int countByProject(Project project);
}

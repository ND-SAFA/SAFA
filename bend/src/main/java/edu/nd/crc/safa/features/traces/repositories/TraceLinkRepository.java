package edu.nd.crc.safa.features.traces.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {
    default List<TraceLink> getLinksInProject(Project project) {
        return findBySourceArtifactProjectId(project.getId());
    }

    List<TraceLink> findBySourceArtifactProjectId(UUID projectId);

    default Optional<TraceLink> getByProjectAndSourceAndTarget(Project project, String sourceName, String targetName) {
        return findBySourceArtifactProjectIdAndSourceArtifactNameAndTargetArtifactName(project.getId(), sourceName, targetName);
    }

    Optional<TraceLink> findBySourceArtifactProjectIdAndSourceArtifactNameAndTargetArtifactName(UUID projectId,
                                                                                                String sourceName,
                                                                                                String targetName);
}

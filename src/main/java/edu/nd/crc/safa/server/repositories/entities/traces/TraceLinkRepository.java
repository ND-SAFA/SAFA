package edu.nd.crc.safa.server.repositories.entities.traces;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkRepository extends CrudRepository<TraceLink, UUID> {
    default List<TraceLink> getLinksInProject(Project project) {
        return findBySourceArtifactProject(project);
    }

    List<TraceLink> findBySourceArtifactProject(Project project);

    default Optional<TraceLink> getByProjectAndSourceAndTarget(Project project, String sourceName, String targetName) {
        return findBySourceArtifactProjectAndSourceArtifactNameAndTargetArtifactName(project, sourceName, targetName);
    }

    Optional<TraceLink> findBySourceArtifactProjectAndSourceArtifactNameAndTargetArtifactName(Project project,
                                                                                              String sourceName,
                                                                                              String targetName);
}

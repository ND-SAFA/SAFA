package edu.nd.crc.safa.server.repositories.traces;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.artifacts.IVersionRepository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceLinkVersionRepository extends CrudRepository<TraceLinkVersion, UUID>,
    IVersionRepository<TraceLinkVersion, TraceAppEntity> {

    default List<TraceLinkVersion> getApprovedLinksInVersion(ProjectVersion projectVersion) {
        return findByProjectVersionAndApprovalStatus(projectVersion, TraceApproval.APPROVED);
    }

    default List<TraceLinkVersion> getApprovedLinksInProject(Project project) {
        return findByProjectVersionProjectAndApprovalStatus(project, TraceApproval.APPROVED);
    }

    default List<TraceLinkVersion> getProjectLinks(Project project) {
        return findByProjectVersionProject(project);
    }

    List<TraceLinkVersion> findByProjectVersionProject(Project project);

    List<TraceLinkVersion> findByTraceLink(TraceLink traceLink);

    List<TraceLinkVersion> findByTraceLinkTraceLinkId(UUID traceLinkId);

    List<TraceLinkVersion> findByProjectVersionProjectAndApprovalStatus(Project project,
                                                                        TraceApproval approvalStatus);

    List<TraceLinkVersion> findByProjectVersionAndApprovalStatus(ProjectVersion projectVersion,
                                                                 TraceApproval approvalStatus);

    default List<TraceLinkVersion> getByProjectVersionAndSourceName(ProjectVersion projectVersion,
                                                                    String name) {
        return findByProjectVersionAndTraceLinkSourceArtifactName(projectVersion, name);
    }

    default List<TraceLinkVersion> getByProjectVersionAndTargetName(ProjectVersion projectVersion,
                                                                    String name) {
        return findByProjectVersionAndTraceLinkSourceArtifactName(projectVersion, name);
    }

    Optional<TraceLinkVersion> findByProjectVersionAndTraceLink(ProjectVersion projectVersion, TraceLink traceLink);
    
    List<TraceLinkVersion> findByProjectVersionAndTraceLinkSourceArtifactName(ProjectVersion projectVersion,
                                                                              String name);
}

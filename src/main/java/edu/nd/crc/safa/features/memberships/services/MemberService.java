package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for CRUD operations related to project memberships
 */
@Service
@AllArgsConstructor
public class MemberService implements IAppEntityService<ProjectMemberAppEntity> {

    ProjectMembershipRepository projectMembershipRepository;

    /**
     * Retrieve project membership with given id. Throws error if not found.
     *
     * @param projectMembershipId ID of membership being retrieved.
     * @return The project membership.
     */
    public ProjectMembership getMembershipById(UUID projectMembershipId) {
        Optional<ProjectMembership> projectMembershipQuery =
            this.projectMembershipRepository.findById(projectMembershipId);
        if (projectMembershipQuery.isEmpty()) {
            throw new SafaError("Could not find membership with id: %s", projectMembershipId);
        }
        return projectMembershipQuery.get();
    }

    @Override
    public List<ProjectMemberAppEntity> getAppEntities(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        return this.projectMembershipRepository.findByProject(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
    }
}

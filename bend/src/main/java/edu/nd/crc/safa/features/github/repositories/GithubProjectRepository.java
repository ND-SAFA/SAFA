package edu.nd.crc.safa.features.github.repositories;

import java.util.Optional;

import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GithubProjectRepository extends JpaRepository<GithubProject, Long> {

    Optional<GithubProject> findByProjectAndOwnerAndRepositoryName(Project project, String owner, String repositoryName);

}

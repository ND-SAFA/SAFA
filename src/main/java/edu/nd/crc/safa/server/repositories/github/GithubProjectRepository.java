package edu.nd.crc.safa.server.repositories.github;

import edu.nd.crc.safa.server.entities.db.GithubProject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GithubProjectRepository extends JpaRepository<GithubProject, Long> {
}

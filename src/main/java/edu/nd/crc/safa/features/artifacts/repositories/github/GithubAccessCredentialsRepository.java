package edu.nd.crc.safa.server.repositories.github;

import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import org.springframework.context.annotation.Scope;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
@Scope("singleton")
public interface GithubAccessCredentialsRepository extends JpaRepository<GithubAccessCredentials, UUID> {

    Optional<GithubAccessCredentials> findByUser(SafaUser user);
}

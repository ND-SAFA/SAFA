package edu.nd.crc.safa.features.github.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.context.annotation.Scope;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
@Scope("singleton")
public interface GithubAccessCredentialsRepository extends JpaRepository<GithubAccessCredentials, UUID> {

    Optional<GithubAccessCredentials> findByUser(SafaUser user);
}

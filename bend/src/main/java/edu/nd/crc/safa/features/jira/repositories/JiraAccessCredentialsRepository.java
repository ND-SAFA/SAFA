package edu.nd.crc.safa.features.jira.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.context.annotation.Scope;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
@Scope("singleton")
public interface JiraAccessCredentialsRepository extends JpaRepository<JiraAccessCredentials, UUID> {

    Optional<JiraAccessCredentials> findByUser(SafaUser user);

}

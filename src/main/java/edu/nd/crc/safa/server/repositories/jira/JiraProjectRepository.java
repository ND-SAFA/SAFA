package edu.nd.crc.safa.server.repositories.jira;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.JiraProject;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JiraProjectRepository extends CrudRepository<JiraProject, UUID> {

}

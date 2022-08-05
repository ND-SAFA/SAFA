package edu.nd.crc.safa.features.jira.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.jira.entities.db.JiraProject;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JiraProjectRepository extends CrudRepository<JiraProject, UUID> {

}

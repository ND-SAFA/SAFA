package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.ParserError;
import edu.nd.crc.safa.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ParserErrorRepository extends CrudRepository<ParserError, UUID> {

    List<ParserError> findByProject(Project project);
}

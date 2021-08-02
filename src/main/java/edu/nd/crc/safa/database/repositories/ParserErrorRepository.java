package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.database.entities.ParserError;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ParserErrorRepository extends CrudRepository<ParserError, UUID> {
}

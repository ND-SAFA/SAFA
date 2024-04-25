package edu.nd.crc.safa.features.comments.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentConceptRepository extends CrudRepository<CommentConcept, UUID> {
}

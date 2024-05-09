package edu.nd.crc.safa.features.comments.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentConceptRepository extends CrudRepository<CommentConcept, UUID> {

    List<CommentConcept> findAllByComment_IdIn(List<UUID> commentIds);
}

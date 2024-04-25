package edu.nd.crc.safa.features.comments.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentArtifactRepository extends CrudRepository<CommentArtifact, UUID> {
}

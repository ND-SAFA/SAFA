package edu.nd.crc.safa.features.comments.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.comments.entities.persistent.Comment;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentRepository extends CrudRepository<Comment, UUID> {
    List<Comment> findByArtifactOrderByCreatedAtAsc(Artifact artifact);
}

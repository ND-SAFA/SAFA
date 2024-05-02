package edu.nd.crc.safa.features.health;

import java.util.List;

import edu.nd.crc.safa.features.comments.entities.persistent.Comment;
import edu.nd.crc.safa.features.comments.entities.persistent.CommentConcept;

@FunctionalInterface
public interface CommentProcessor<T> {
    T process(Comment comment, List<CommentConcept> concepts);
}

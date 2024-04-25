package edu.nd.crc.safa.features.comments.entities.persistent;

import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Data
@Entity
@Table(name = "comment_concept")
public class CommentConcept {
    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column(nullable = false)
    private UUID id;
    /**
     * The concept associated with comment.
     */
    @Column(name = "concept_name")
    private String conceptName;

    /**
     * Author of comment
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "comment_id", nullable = false)
    private Comment comment;
}

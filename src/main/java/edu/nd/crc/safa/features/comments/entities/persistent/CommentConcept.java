package edu.nd.crc.safa.features.comments.entities.persistent;

import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Entity
@Table(name = "comment_concept")
public class CommentConcept {
    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column(nullable = false)
    private UUID id;
    /**
     * Author of comment
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "comment_id", nullable = false)
    private Comment comment;
    /**
     * The concept associated with comment.
     */
    @Column(name = "concept_name")
    private String conceptName;

    public CommentConcept(Comment comment, String conceptName) {
        this.comment = comment;
        this.conceptName = conceptName;
    }

    /**
     * @return Hash of ID.
     */
    public int hashCode() {
        return this.id.hashCode();
    }

    /**
     * @param obj Object being compared.
     * @return True if IDs match.
     */
    @Override
    public boolean equals(Object obj) {
        if (obj instanceof CommentConcept commentConcept) {
            return this.id.equals(commentConcept.id);
        }
        return false;
    }
}

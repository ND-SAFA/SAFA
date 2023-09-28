package edu.nd.crc.safa.features.attributes.entities.db.layouts;

import java.util.UUID;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

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

@Entity
@Table(name = "artifact_type_to_layout")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class ArtifactTypeToLayoutMapping {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "layout_id", nullable = false)
    private AttributeLayout layout;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_type_id", nullable = false)
    private ArtifactType artifactType;

    public ArtifactTypeToLayoutMapping(AttributeLayout layout, ArtifactType type) {
        this.layout = layout;
        this.artifactType = type;
    }
}

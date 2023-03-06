package edu.nd.crc.safa.features.attributes.entities.db.layouts;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.types.ArtifactType;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "artifact_type_to_layout")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class ArtifactTypeToLayoutMapping {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
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

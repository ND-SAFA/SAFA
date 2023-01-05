package edu.nd.crc.safa.features.attributes.entities.db.definitions;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "custom_attribute",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {"keyname", "project_id"},
            name = AppConstraints.UNIQUE_KEYNAME_PER_PROJECT)
    }
)
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class CustomAttribute {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(nullable = false)
    @Enumerated(EnumType.ORDINAL)
    private CustomAttributeType type;

    @Column(nullable = false)
    private String keyname;

    @Column(nullable = false)
    private String label;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

}

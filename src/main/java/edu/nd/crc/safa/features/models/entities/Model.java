package edu.nd.crc.safa.features.models.entities;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Type;

/**
 * Represents the database entity for a trace generation model
 */
@Entity
@Table(name = "trace_generation_model")
@Getter
@Setter
@NoArgsConstructor
public class Model {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID id;
    @Column
    String name;
    @Column
    @Enumerated(EnumType.STRING)
    BaseGenerationModels baseModel;

    public Model(ModelAppEntity modelAppEntity) {
        this.id = modelAppEntity.getId();
        this.name = modelAppEntity.getName();
        this.baseModel = modelAppEntity.getBaseModel();
    }
}

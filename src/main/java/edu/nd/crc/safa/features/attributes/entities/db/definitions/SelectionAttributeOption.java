package edu.nd.crc.safa.features.attributes.entities.db.definitions;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "selection_attribute_option")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class SelectionAttributeOption {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(name = "option_value", nullable = false)
    private String value;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_id", nullable = false)
    private CustomAttribute attribute;

    public SelectionAttributeOption(CustomAttribute attribute, String value) {
        this.attribute = attribute;
        this.value = value;
    }

}

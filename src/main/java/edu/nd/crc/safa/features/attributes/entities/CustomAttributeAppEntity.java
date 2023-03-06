package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * This is the front-end representation of an attribute's definition.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CustomAttributeAppEntity {

    @NotNull
    @NotEmpty
    private String key;

    @NotNull
    @NotEmpty
    private String label;

    @NotNull
    private CustomAttributeType type;

    private List<String> options;

    private Number min;

    private Number max;

    public CustomAttributeAppEntity(String key, String label, CustomAttributeType type) {
        this.key = key;
        this.label = label;
        this.type = type;
        this.options = null;
        this.min = null;
        this.max = null;
    }
}

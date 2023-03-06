package edu.nd.crc.safa.features.attributes.entities;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AttributePositionAppEntity {

    @NotNull
    @NotEmpty
    private String key;

    @NotNull
    private int x;

    @NotNull
    private int y;

    @NotNull
    private int width;

    @NotNull
    private int height;

}

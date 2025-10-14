package edu.nd.crc.safa.features.layout;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Settings involved for setting the layout generation.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class LayoutSettings {
    public static final int ARTIFACT_WIDTH = 225;
    public static final int ARTIFACT_HEIGHT = 200;
    public static final String LAYOUT_ALGORITHM = "org.eclipse.elk.mrtree";
}

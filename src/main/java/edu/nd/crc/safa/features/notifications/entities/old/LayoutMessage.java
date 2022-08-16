package edu.nd.crc.safa.features.notifications.entities.old;

import java.util.UUID;
import javax.annotation.Nullable;

import edu.nd.crc.safa.features.notifications.entities.old.layout.LayoutEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Layout message can alert user that:
 * - Document layout has changed
 * - Entire project layout has changed
 * - Default artifact tree has changed
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class LayoutMessage {

    /**
     * The layout entity being affected.
     */
    LayoutEntity type;
    /**
     * The document id if LayoutEntity = DOCUMENT and document not default artifact tree.
     */
    @Nullable
    UUID documentId;
    /**
     * The user initiating this message
     */
    String user;
}

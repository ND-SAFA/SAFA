package edu.nd.crc.safa.features.notifications;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class ErrorMessage {
    private final String type = "error";
    String message;
}

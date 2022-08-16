package edu.nd.crc.safa.utilities;

import java.util.Optional;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.reactive.function.client.WebClientException;
import reactor.core.publisher.Mono;

/**
 * Helper methods used when connecting Safa to external API services.
 * Defined abstract, so it cannot be instantiated.(removes the need to a private constructor)
 */
public abstract class WebApiUtils {

    private static final Logger log = LoggerFactory.getLogger(WebApiUtils.class);

    public static <T> Optional<T> blockOptional(Mono<T> mono) {
        try {
            return mono.blockOptional();
        } catch (WebClientException ex) {
            log.error("Exception thrown while executing blocking call", ex);
            throw new SafaError("Exception thrown while executing blocking call", ex);
        }
    }
}

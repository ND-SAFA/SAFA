package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.server.entities.api.SafaError;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.reactive.function.client.WebClientException;
import reactor.core.publisher.Mono;

import java.util.Optional;

/**
 * Helper methods used when connecting Safa to external API services.
 *
 * Abstract so it cannot be instantiated
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

package edu.nd.crc.safa.utilities;

import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Wrapper over {@link ThreadPoolTaskExecutor} to catch exceptions and set up the error result
 */
@AllArgsConstructor
public class ExecutorDelegate {

    private static final Logger logger = LoggerFactory.getLogger(ExecutorDelegate.class);
    private ThreadPoolTaskExecutor executor;

    public <T> DeferredResult<T> createOutput(Long timeout) {
        return new DeferredResult<>(timeout);
    }

    public <T> void submit(DeferredResult<T> output, ExecutorTask task) {
        executor.submit(() -> {
            try {
                task.run();
            } catch (Exception e) {
                logger.error("Intercepted the following exception: ", e);
                output.setErrorResult(e);
            }
        });
    }
}

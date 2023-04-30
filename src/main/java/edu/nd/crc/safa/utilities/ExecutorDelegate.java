package edu.nd.crc.safa.utilities;

import lombok.AllArgsConstructor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Wrapper over {@link ThreadPoolTaskExecutor} to catch exceptions and set up the error result
 */
@AllArgsConstructor
public class ExecutorDelegate {

    private ThreadPoolTaskExecutor executor;

    public <T> DeferredResult<T> createOutput(Long timeout) {
        return new DeferredResult<>(timeout);
    }

    public <T> void submit(DeferredResult<T> output, ExecutorTask task) {
        executor.submit(() -> {
            try {
                task.run();
            } catch (Exception e) {
                output.setErrorResult(e);
            }
        });
    }
}

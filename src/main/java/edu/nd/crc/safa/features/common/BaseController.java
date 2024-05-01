package edu.nd.crc.safa.features.common;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;
import edu.nd.crc.safa.utilities.exception.ExternalAPIException;
import edu.nd.crc.safa.utilities.exception.InvalidTokenException;
import edu.nd.crc.safa.utilities.exception.UserError;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.apache.tomcat.util.http.fileupload.impl.FileSizeLimitExceededException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.util.function.ThrowingConsumer;
import org.springframework.util.function.ThrowingFunction;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.async.DeferredResult;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@RestController
@AllArgsConstructor
public abstract class BaseController {

    private static final long DEFAULT_REQUEST_TIMEOUT = 5000L;

    @Getter(AccessLevel.PROTECTED)
    private final ResourceBuilder resourceBuilder;
    @Getter(AccessLevel.PROTECTED)
    private final ServiceProvider serviceProvider;

    @ExceptionHandler(FileSizeLimitExceededException.class)
    public SafaError handleFileSizeLimitExceeded(FileSizeLimitExceededException exception) {
        exception.printStackTrace();
        return new SafaError("%s is too big. Please contact SAFA administrators.", exception.getFileName());
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public SafaError handleFileSizeLimitExceeded(MaxUploadSizeExceededException exception) {
        exception.printStackTrace();
        return new SafaError("Upload exceeded max size of. Please contact SAFA administrators.");
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleValidationError(MethodArgumentNotValidException exception) {
        BindingResult bindingResult = exception.getBindingResult();
        StringBuilder errorMessage = new StringBuilder();
        for (ObjectError error : bindingResult.getAllErrors()) {
            errorMessage.append(createValidationMessage(error)).append("\n");
        }
        return new SafaError(errorMessage.toString());
    }

    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleArgumentTypeError(MethodArgumentTypeMismatchException exception) {
        return new SafaError("Failed to dispatch request: " + exception.getMostSpecificCause().getMessage());
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
        exception.printStackTrace();
        String errorMessage = AppConstraints.getConstraintError(exception);
        return new SafaError(errorMessage, exception);
    }

    @ExceptionHandler(SafaError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleServerError(SafaError safaError) {
        safaError.printError();
        return safaError;
    }

    @ExceptionHandler(SafaItemNotFoundError.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public SafaItemNotFoundError handleServerError(SafaItemNotFoundError safaError) {
        return safaError;
    }

    @ExceptionHandler(ExternalAPIException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    public ExternalAPIException handleExternalApiException(ExternalAPIException ex) {
        return ex;
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleBadRequest(HttpMessageNotReadableException ex) {
        return new SafaError(ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Exception handleGenericError(Exception ex) {
        ex.printStackTrace();
        return new SafaError(ex.getMessage(), ex);
    }

    @ExceptionHandler(MissingPermissionException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public MissingPermissionException handleMissingPermission(MissingPermissionException ex) {
        return ex;
    }

    @ExceptionHandler(InvalidTokenException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public InvalidTokenException handleExpiredToken(InvalidTokenException ex) {
        return ex;
    }

    @ExceptionHandler(UserError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public UserError handleUserError(UserError ex) {
        return ex;
    }

    private String createValidationMessage(ObjectError error) {
        String objectName = error.getObjectName();
        String message = error.getDefaultMessage();
        if (error instanceof FieldError) {
            String fieldName = ((FieldError) error).getField();
            return fieldName + " in " + objectName + " " + message;
        } else {
            return objectName + message;
        }
    }

    /**
     * Perform a deferred request which will make the request in the background.
     *
     * @param request The request to make.
     * @param <T>     The desired output type.
     * @return A deferred result that will perform the request.
     */
    protected <T> DeferredResult<T> makeDeferredRequest(ThrowingFunction<SafaUser, T> request) {
        return makeDeferredRequest(request, BaseController.DEFAULT_REQUEST_TIMEOUT);
    }

    /**
     * Perform a deferred request which will make the request in the background.
     *
     * @param request The request to make.
     * @return A deferred result that will perform the request.
     */
    protected DeferredResult<Void> makeDeferredRequest(ThrowingConsumer<SafaUser> request) {
        return makeDeferredRequest(request, BaseController.DEFAULT_REQUEST_TIMEOUT);
    }

    /**
     * Perform a deferred request which will make the request in the background.
     *
     * @param request The request to make.
     * @param timeout The timeout for the request.
     * @return A deferred result that will perform the request.
     */
    protected DeferredResult<Void> makeDeferredRequest(ThrowingConsumer<SafaUser> request, long timeout) {
        return makeDeferredRequest((user) -> {
            request.accept(user);
            return null;
        }, timeout);
    }

    /**
     * Perform a deferred request which will make the request in the background.
     *
     * @param request The request to make.
     * @param timeout The timeout for the request.
     * @param <T>     The desired output type.
     * @return A deferred result that will perform the request.
     */
    protected <T> DeferredResult<T> makeDeferredRequest(ThrowingFunction<SafaUser, T> request, long timeout) {

        ExecutorDelegate executorDelegate = serviceProvider.getExecutorDelegate();
        SafaUserService safaUserService = serviceProvider.getSafaUserService();

        DeferredResult<T> output = executorDelegate.createOutput(timeout);

        SafaUser user = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            T result = request.apply(user, SafaError::new);
            output.setResult(result);
        });

        return output;
    }

    protected SafaUser getCurrentUser() {
        return getServiceProvider().getSafaUserService().getCurrentUser();
    }
}

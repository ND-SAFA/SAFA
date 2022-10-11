package edu.nd.crc.safa.features.common;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.utilities.exception.ExternalAPIException;

import lombok.AllArgsConstructor;
import org.apache.tomcat.util.http.fileupload.impl.FileSizeLimitExceededException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@RestController
@AllArgsConstructor
public abstract class BaseController {

    protected final ResourceBuilder resourceBuilder;
    protected final ServiceProvider serviceProvider;

    protected Document getDocumentById(DocumentRepository documentRepository,
                                       UUID documentId) throws SafaError {
        Optional<Document> documentOptional = documentRepository.findById(documentId);
        if (documentOptional.isPresent()) {
            return documentOptional.get();
        } else {
            throw new SafaError("Could not find document with id: %s", documentId);
        }
    }

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

    @ExceptionHandler(ExternalAPIException.class)
    public ResponseEntity<SafaError> handleExternalApiException(ExternalAPIException ex) {
        return ResponseEntity
            .status(ex.getStatus())
            .body(new SafaError(ex.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleGenericError(Exception ex) {
        ex.printStackTrace();
        return new SafaError("An unexpected server error occurred.", ex);
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
}

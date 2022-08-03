package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;

import lombok.AllArgsConstructor;
import org.apache.tomcat.util.http.fileupload.impl.FileSizeLimitExceededException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
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

    protected Document getDocumentById(DocumentRepository documentRepository,
                                       UUID documentId) throws SafaError {
        Optional<Document> documentOptional = documentRepository.findById(documentId);
        if (documentOptional.isPresent()) {
            return documentOptional.get();
        } else {
            throw new SafaError("Could not find document with given id:" + documentId);
        }
    }

    @ExceptionHandler(FileSizeLimitExceededException.class)
    public SafaError handleFileSizeLimitExceeded(FileSizeLimitExceededException exception) {
        exception.printStackTrace();
        String errorMessage = exception.getFileName() + " is too big. Please contact SAFA administrators.";
        return new SafaError(errorMessage, exception);
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public SafaError handleFileSizeLimitExceeded(MaxUploadSizeExceededException exception) {
        exception.printStackTrace();
        String errorMessage = "Upload exceeded max size of " + exception.getMaxUploadSize()
            + ". Please contact SAFA administrators.";
        return new SafaError(errorMessage, exception);
    }

    @ExceptionHandler(SafaError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleServerError(SafaError safaError) {
        safaError.printError();
        return safaError;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleValidationError(MethodArgumentNotValidException exception) {
        BindingResult bindingResult = exception.getBindingResult();
        StringBuilder errorMessage = new StringBuilder();
        for (ObjectError error : bindingResult.getAllErrors()) {
            errorMessage.append(createValidationMessage(error)).append("\n");
        }
        SafaError error = new SafaError(errorMessage.toString());
        return error;
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public SafaError handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
        exception.printStackTrace();
        String errorMessage = AppConstraints.getConstraintError(exception);
        return new SafaError(errorMessage, exception);
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

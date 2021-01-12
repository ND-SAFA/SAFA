package edu.nd.crc.safa.importer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Base64;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import com.jsoniter.JsonIterator;
import org.springframework.stereotype.Component;

@Component
public class UploadFlatfile {

  public class ParsedFiles {
    private List<String> requiredFiles;
    private List<GeneratedFiles> generatedFiles;

    public ParsedFiles(List<String> requiredFiles, List<GeneratedFiles> generatedFiles){
      this.requiredFiles = requiredFiles;
      this.generatedFiles = generatedFiles;
    }

    public List<String> getRequired(){
      return requiredFiles;
    }

    public List<GeneratedFiles> getGenerated(){
      return generatedFiles;
    }
  }

  public class GeneratedFiles {
    private final String filename;
    private final String source;
    private final String target;

    public GeneratedFiles(String filename, String source, String target) {
      this.filename = filename;
      this.source = source;
      this.target = target;
    }

    public String getName(){
      return filename;
    }

    public String getSource(){
      return source;
    }

    public String getTarget(){
      return target;
    }
  }

  public void uploadFile(String projId, String jsonfiles) throws Exception {
    createFlatfilesDir();
    
    JsonIterator iterator = JsonIterator.parse(jsonfiles);
    for (String filename = iterator.readObject(); filename != null; filename = iterator.readObject()){
      String encodedData = iterator.readString();
      byte[] bytes = Base64.getDecoder().decode(encodedData);
      String fullPath = "/flatfilesDir/" + filename; 
      Files.write(Paths.get(fullPath), bytes);
    }
  }

  public String getMissingFiles(String projId) throws Exception {
    File myDir = createFlatfilesDir();

    ParsedFiles parsedfiles = parseTim("/flatfilesDir");
    List<String> uploadedFiles = Arrays.asList(myDir.list());

    String data = createMissingFilesJson(uploadedFiles, parsedfiles.getRequired());
    
    System.out.println(data);
    return String.format("{ \"success\": true, \"message\": \"Checking missing files successful.\", \"data\": %s }", data);
  }

  public String clearFlatfileDir() throws Exception {
    File myDir = createFlatfilesDir();
    File[] fileList = myDir.listFiles();
    
    if (fileList.length > 0){
      if (deleteDirectory(myDir)){
        createFlatfilesDir();
        return "{ \"success\": true, \"message\": \"Directory has successfully been cleared.\"}";
      } 
      else {
        return "{ \"success\": false, \"message\": \"Directory could not be cleared.\"}";
      }
    }

    return "{ \"success\": true, \"message\": \"Directory has already been cleared.\"}";
  }

  public boolean deleteDirectory(File dir) throws Exception {
    File[] files = dir.listFiles();
    if (files != null) {
      for (File file : files) {
        deleteDirectory(file);
      }
    }
    return dir.delete();
  }
  
  public ParsedFiles parseTim(String dirName) throws Exception {
    String fileName = dirName + '/' + "tim.json";
    File tim = new File(fileName);
    if (!tim.exists()){
      throw new Exception("Please upload a tim.json file");
    }

    String data = new String(Files.readAllBytes(Paths.get(fileName)));
    JsonIterator iterator = JsonIterator.parse(data);

    List<String> requiredFiles = new ArrayList<String>();
    List<GeneratedFiles> generatedFiles = new ArrayList<GeneratedFiles>();

    requiredFiles.add("tim.json");
    for (String field = iterator.readObject(); field != null; field = iterator.readObject()){
      if (field.equals("DataFiles")) {
        for (String artifact = iterator.readObject(); artifact != null; artifact = iterator.readObject()){
          for (String file = iterator.readObject(); file != null; file = iterator.readObject()){
            requiredFiles.add(iterator.readString());
          }
        }
      }
      else {
        addLinkFile(iterator, requiredFiles, generatedFiles);
      }
    }
    return new ParsedFiles(requiredFiles, generatedFiles);
  }

  public void addLinkFile(JsonIterator iterator, List<String> requiredFiles, List<GeneratedFiles> generatedFiles) throws Exception {
    String filename = "";
    String source = "";
    String target = "";
    Boolean val = false;

    for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()){
      if (attr.equals("File")){
        filename = iterator.readString();
      }

      if (attr.equals("Source")){
        source = iterator.readString();
      }

      if (attr.equals("Target")){
        target = iterator.readString();
      }

      if (attr.equals("generateLinks")){
        val = iterator.readString().equals("True") ? true : false;
      }
    }

    if (val){
      generatedFiles.add(new GeneratedFiles(filename,source,target));
    }
    else {
      requiredFiles.add(filename);
    }
  }
  
  public String createJsonArray(List<String> files) {
    String jsonArr = "";

    if (files.size() == 0){
      return "[]";
    }

    else if (files.size() == 1){
      return String.format("[\"%s\"]", files.get(0));
    }
    
    else {
      for (int i = 0; i < files.size(); i++){
        if (i == 0){
          jsonArr += "[\"" + files.get(i) + "\"";
        } 
        else if (i == files.size() - 1){
          jsonArr += ",\"" + files.get(i) + "\"]";
        }
        else {
          jsonArr += ",\"" + files.get(i) + "\"";
        }
      }
    }

    return jsonArr;
  }
    
  
  public String createMissingFilesJson(List<String> uploadedFiles, List<String> requiredFiles){
    return "{\"uploadedFiles\":" + createJsonArray(uploadedFiles) + ",\"expectedFiles\":" + createJsonArray(requiredFiles) + "}";
  }
  
  public File createFlatfilesDir() throws Exception{
    String dir = "/flatfilesDir";
    File myDir = new File(dir);

    if (!myDir.exists()) {
      if (!myDir.mkdirs()){
        throw new Exception("Error creating Flatfile folder: Path: /flatfilesDir");
      }
    }

    if (!myDir.isDirectory()) {
      if (!myDir.delete()){
        throw new Exception("Error deleting Flatfile file: Path: /flatfilesDir");
      }
      if (!myDir.mkdirs()){
        throw new Exception("Error creating Flatfile folder: Path: /flatfilesDir");
      }
    }

    return myDir;
  }
}

/**
 * Returns given string with newlines inserted after maxWordCount
 * has been reached
 * @param str - The original string.
 * @param maxWordCount  - The maximum number of words to have per line.
 * @returns string
 */
export function splitIntoLines(str: string, maxWordCount: number): string {
  const words: string[] = str.split(" ");
  let finalString = "";
  let count = 0;
  words.forEach((w) => {
    if (count < maxWordCount) {
      finalString += w + " ";
      count++;
    } else {
      finalString += w + "\n";
      count = 0;
    }
  });
  return finalString;
}

export function capitalize(blob: string): string {
  return blob.charAt(0).toUpperCase() + blob.slice(1);
}

export function getArtifactTypePrintName(type: string): string {
  if (type === undefined) {
    return "Unknown type";
  }
  switch (type.toLowerCase()) {
    case "requirement":
      return "Requirements";
    case "design":
      return "Designs";
    case "hazard":
      return "Hazards";
    case "environmentalassumption":
      return "Environmental Assumptions";
    case "safetyrequirement":
      return "Safety Requirement";
    default:
      return capitalize(type.toLowerCase());
  }
}

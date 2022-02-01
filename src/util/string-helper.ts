/**
 * Returns given string with newlines inserted after maxWordCount
 * has been reached.
 *
 * @param str - The original string.
 * @param maxWordCount - The maximum number of words to have per line.
 *
 * @returns The updated input string.
 */
export function splitIntoLines(str: string, maxWordCount: number): string {
  const words = str.split(" ");
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

/**
 * Capitalizes the first letter of the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Capitalizes the first letter of all words in the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
export function capitalizeSentence(str: string): string {
  return str
    .split(" ")
    .map((word) => capitalize(word))
    .join(" ");
}

/**
 * @deprecated Remove when project creator done.
 *
 * Returns the sentence case name of the artifact type.
 *
 * @param type - The type to stringify.
 *
 * @return The sentence case type name.
 */
export function getArtifactTypePrintName(type?: string): string {
  const nameMap: Record<string, string> = {
    requirement: "Requirements",
    design: "Designs",
    hazard: "Hazards",
    environmentalassumption: "Environmental Assumptions",
    safetyrequirement: "Safety Requirement",
  };

  return type
    ? nameMap[type.toLowerCase()] || capitalizeSentence(type.toLowerCase())
    : "Unknown Type";
}

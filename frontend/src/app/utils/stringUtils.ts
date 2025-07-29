/**
 * Truncates a string to a specified number of lines with optional max length.
 * Adds line breaks and an ellipsis if truncated.
 */
export const truncateLines = (
  str: string,
  options?: { lines?: number; maxLength?: number }
): string => {
  const { lines = 2, maxLength = 50 } = options ?? {};

  if (!str) return "N/A";
  if (str.length <= maxLength) return str;

  const segmentLength = Math.floor(maxLength / lines);
  let result = "";

  for (let i = 1; i < lines; i++) {
    const start = i * segmentLength;
    const end = start + segmentLength;
    result += str.slice(start, end);
    if (i < lines - 1) result += "\n";
  }

  return result + "...";
};

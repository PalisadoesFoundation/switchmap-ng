/**
 * Formats a Unix timestamp (in seconds) into a human-readable date and time string.
 * 
 * @param timestamp - The Unix timestamp in seconds. Can be a number or a string.
 * 
 * @remarks
 * If the timestamp is invalid, undefined, null, or non-positive, the function returns "Unknown".
 * Otherwise, it converts the timestamp to a Date object and formats it using the
 * user's local date and time settings.
 * @returns A formatted date and time string or "Unknown" for invalid inputs.
 */
export const formatUnixTimestamp = (timestamp?: string | number | null): string => {
  if (!timestamp) return "Unknown";

  const tsNumber = typeof timestamp === "string" ? Number(timestamp) : timestamp;

  if (isNaN(tsNumber) || tsNumber <= 0) return "Unknown";

  const date = new Date(tsNumber * 1000);
  return date.toLocaleString();
}

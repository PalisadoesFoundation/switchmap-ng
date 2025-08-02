export const formatUnixTimestamp = (timestamp?: string | number | null): string => {
  if (!timestamp) return "Unknown";

  const tsNumber = typeof timestamp === "string" ? Number(timestamp) : timestamp;

  if (isNaN(tsNumber) || tsNumber <= 0) return "Unknown";

  const date = new Date(tsNumber * 1000);
  return date.toLocaleString();
}

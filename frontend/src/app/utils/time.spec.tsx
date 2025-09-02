import { describe, it, expect } from "vitest";
import { formatUptime } from "./time";

describe("formatUptime", () => {
  it("formats zero hundredths correctly", () => {
    expect(formatUptime(0)).toBe("0d 0h 0m 0s");
  });

  it("formats seconds correctly", () => {
    expect(formatUptime(100)).toBe("0d 0h 0m 1s"); // 100 hundredths = 1 second
  });

  it("formats minutes correctly", () => {
    expect(formatUptime(6100)).toBe("0d 0h 1m 1s"); // 6100 hundredths = 61 seconds
  });

  it("formats hours correctly", () => {
    expect(formatUptime(366000)).toBe("0d 1h 1m 0s"); // 366000 hundredths = 1h 1m
  });

  it("formats days correctly", () => {
    expect(formatUptime(9006100)).toBe("1d 1h 1m 1s"); // 9006100 hundredths = 1d 1h 1m 1s
  });
});

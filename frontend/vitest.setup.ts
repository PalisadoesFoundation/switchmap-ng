// vitest.setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Polyfill ResizeObserver for Recharts
class ResizeObserver {
  callback: ResizeObserverCallback;
  constructor(callback: ResizeObserverCallback) {
    this.callback = callback;
  }
  observe() {
    // no-op
  }
  unobserve() {
    // no-op
  }
  disconnect() {
    // no-op
  }
}

(global as any).ResizeObserver = ResizeObserver;

// Mock Next.js App Router hooks
vi.mock('next/navigation', () => {
  return {
    useRouter: () => ({
      push: vi.fn(),
      replace: vi.fn(),
      prefetch: vi.fn(),
    }),
    usePathname: () => '',
    useSearchParams: () => new URLSearchParams(),
  };
});

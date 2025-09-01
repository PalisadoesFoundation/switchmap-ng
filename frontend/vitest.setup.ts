// vitest.setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import React from 'react';
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

// Global mocks
vi.mock('next/navigation', () => ({ useRouter: () => ({ push: vi.fn() }) }));
vi.mock('next-themes', () => ({ useTheme: () => ({ theme: 'light' }) }));

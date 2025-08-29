import '@testing-library/jest-dom';

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

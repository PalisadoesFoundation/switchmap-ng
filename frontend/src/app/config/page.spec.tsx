import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  within,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ConfigPage, { __resetConfigCache } from "./page";

// Mock the Sidebar component
vi.mock("../components/Sidebar", () => ({
  Sidebar: () => <div data-testid="sidebar">Sidebar</div>,
}));

// Mock react-icons
vi.mock("react-icons/fi", () => ({
  FiCheck: () => <div data-testid="check-icon">✓</div>,
  FiEdit2: () => <div data-testid="edit-icon">✏</div>,
  FiMinus: () => <div data-testid="minus-icon">-</div>,
  FiTrash2: () => <div data-testid="trash-icon">🗑</div>,
  FiChevronDown: () => <div data-testid="chevron-down">⌄</div>,
  FiChevronUp: () => <div data-testid="chevron-up">⌃</div>,
}));

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock window.prompt and alert
Object.defineProperty(window, "prompt", {
  writable: true,
  value: vi.fn(),
});

Object.defineProperty(window, "alert", {
  writable: true,
  value: vi.fn(),
});

const mockConfig = {
  poller: {
    zones: [
      {
        zone: "test-zone-1",
        hostnames: ["host1.example.com", "host2.example.com"],
      },
      {
        zone: "test-zone-2",
        hostnames: ["host3.example.com"],
      },
    ],
    snmp_groups: [
      {
        enabled: true,
        group_name: "Test Group 1",
        snmp_ip: "192.168.1.1",
        snmp_version: 3,
        snmp_secname: "testuser",
        snmp_authprotocol: "SHA",
        snmp_authpassword: "testpass",
        snmp_privprotocol: "AES",
        snmp_privpassword: "testpriv",
        snmp_community: "public",
      },
    ],
  },
  core: {
    debug: "false",
    log_level: "info",
  },
  server: {
    port: "8080",
    host: "localhost",
    db_pass: "1",
  },
};

describe("ConfigPage", () => {
  const user = userEvent.setup();

  beforeEach(() => {
    __resetConfigCache();
    vi.clearAllMocks();
  });

  afterEach(() => {
    __resetConfigCache();
    vi.restoreAllMocks();
  });

  // ---------- Intial Loading ----------

  describe("Initial Loading", () => {
    it("shows loading state initially", () => {
      mockFetch.mockImplementation(() => new Promise(() => {})); // Never resolves

      render(<ConfigPage />);

      expect(screen.getByText("Loading…")).toBeInTheDocument();
      expect(screen.getByText("Switchmap Config")).toBeInTheDocument();
    });

    it("handles fetch error gracefully", async () => {
      const consoleSpy = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});
      mockFetch.mockRejectedValueOnce(new Error("Network error"));

      render(<ConfigPage />);

      await waitFor(() => {
        expect(screen.getByText("Error loading config")).toBeInTheDocument();
      });

      expect(consoleSpy).toHaveBeenCalledWith(
        "Failed to fetch config:",
        expect.any(Error)
      );

      consoleSpy.mockRestore();
    });
    it("handles fetch non-ok response", async () => {
      const consoleSpy = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});
      (fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({}),
      });

      render(<ConfigPage />);

      await waitFor(() => {
        expect(screen.getByText("Error loading config")).toBeInTheDocument();
      });

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  // ---------- Tab Navigation ----------

  describe("Tab Navigation", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );
    });

    it("renders all tabs", () => {
      expect(screen.getByRole("button", { name: "Zones" })).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: "SNMP Groups" })
      ).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: "Advanced" })
      ).toBeInTheDocument();
    });

    it("switches between tabs", async () => {
      expect(screen.getByText("test-zone-1")).toBeInTheDocument();
      await user.click(screen.getByRole("button", { name: "SNMP Groups" }));
      expect(screen.getByText("Test Group 1")).toBeInTheDocument();
      await user.click(screen.getByRole("button", { name: "Advanced" }));
      expect(screen.getByText("Core")).toBeInTheDocument();
      expect(screen.getByText("Server")).toBeInTheDocument();
    });
  });

  // ---------- Zone Tab ----------

  describe("Zones Tab", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );
    });

    it("displays zones correctly", () => {
      expect(screen.getByText("test-zone-1")).toBeInTheDocument();
      expect(screen.getByText("test-zone-2")).toBeInTheDocument();
    });

    it("expands and collapses zones", async () => {
      const expandButton = screen.getAllByTestId("chevron-down")[0];
      await user.click(expandButton);

      expect(screen.getByText("host1.example.com")).toBeInTheDocument();
      expect(screen.getByText("host2.example.com")).toBeInTheDocument();

      const collapseButton = screen.getByTestId("chevron-up");
      await user.click(collapseButton);

      expect(screen.queryByText("host2.example.com")).not.toBeInTheDocument();
    });

    it("enters edit mode for zones", async () => {
      const editButton = screen.getAllByTestId("edit-icon")[0];
      await user.click(editButton);
      const addDeviceButton = screen.getByText("+ Add Device");
      await user.click(addDeviceButton);

      await waitFor(() => {
        const inputs = screen.getAllByPlaceholderText("Enter hostname");
        expect(inputs).toHaveLength(3);
        expect(inputs[0]).toHaveValue("host1.example.com");
        expect(inputs[1]).toHaveValue("host2.example.com");
      });
    });

    it("edits hostname in zone", async () => {
      const editButton = screen.getAllByTestId("edit-icon")[0];
      await user.click(editButton);

      await waitFor(() => {
        const inputs = screen.getAllByPlaceholderText("Enter hostname");
        expect(inputs[0]).toBeInTheDocument();
      });

      const hostInput = screen.getAllByPlaceholderText("Enter hostname")[0];
      await user.clear(hostInput);
      await user.type(hostInput, "new-hostname.example.com");

      expect(hostInput).toHaveValue("new-hostname.example.com");
    });

    it("adds new device to zone", async () => {
      const editButton = screen.getAllByTestId("edit-icon")[0];
      await user.click(editButton);

      await waitFor(() => {
        expect(screen.getByText("+ Add Device")).toBeInTheDocument();
      });

      const addButton = screen.getByText("+ Add Device");
      await user.click(addButton);

      const inputs = screen.getAllByPlaceholderText("Enter hostname");
      expect(inputs).toHaveLength(3);
      expect(inputs[2]).toHaveValue("");
    });

    it("removes device from zone", async () => {
      const editButton = screen.getAllByTestId("edit-icon")[0];
      await user.click(editButton);

      await waitFor(() => {
        const minusButtons = screen.getAllByTestId("minus-icon");
        expect(minusButtons).toHaveLength(2);
      });

      const minusButton = screen.getAllByTestId("minus-icon")[0];
      await user.click(minusButton);

      const inputs = screen.getAllByPlaceholderText("Enter hostname");
      expect(inputs).toHaveLength(1);
    });

    it("deletes entire zone", async () => {
      const deleteButton = screen.getAllByTestId("trash-icon")[0];
      await user.click(deleteButton);

      expect(screen.queryByText("test-zone-1")).not.toBeInTheDocument();
      expect(screen.getByText("test-zone-2")).toBeInTheDocument();
    });

    it("adds new zone", async () => {
      const addZoneButton = screen.getByText("+ Add Zone");
      await user.click(addZoneButton);

      const input = screen.getByPlaceholderText("Zone name");
      await user.type(input, "new-test-zone");

      const addButton = screen.getByText("Add");
      await user.click(addButton);

      expect(screen.getByText("new-test-zone")).toBeInTheDocument();
    });

    it("adds new zone with Enter key", async () => {
      const addZoneButton = screen.getByText("+ Add Zone");
      await user.click(addZoneButton);

      const input = screen.getByPlaceholderText("Zone name");
      await user.type(input, "keyboard-zone{enter}");

      expect(screen.getByText("keyboard-zone")).toBeInTheDocument();
    });

    it("cancels adding new zone", async () => {
      const addZoneButton = screen.getByText("+ Add Zone");
      await user.click(addZoneButton);

      const cancelButton = screen.getByText("Cancel");
      await user.click(cancelButton);

      expect(
        screen.queryByPlaceholderText("Zone name")
      ).not.toBeInTheDocument();
    });
  });

  // ---------- SNMP Groups Tab ----------
  describe("SNMP Groups Tab", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );

      await user.click(screen.getByRole("button", { name: "SNMP Groups" }));
    });

    it("displays SNMP groups correctly", () => {
      expect(screen.getByText("Test Group 1")).toBeInTheDocument();
      expect(screen.getByText("192.168.1.1")).toBeInTheDocument();
    });

    it("expands SNMP group to show all fields", async () => {
      const expandButton = screen.getByTestId("chevron-down");
      await user.click(expandButton);

      expect(screen.getByDisplayValue("Test Group 1")).toBeInTheDocument();
      expect(screen.getByDisplayValue("192.168.1.1")).toBeInTheDocument();
      expect(screen.getByDisplayValue("testuser")).toBeInTheDocument();
      expect(screen.getByRole("checkbox", { name: "Enabled" })).toBeChecked();
    });

    it("enters edit mode for SNMP group", async () => {
      const editButton = screen.getByTestId("edit-icon");
      await user.click(editButton);
      await waitFor(() => {
        const groupNameInput = screen.getByDisplayValue("Test Group 1");
        expect(groupNameInput).not.toHaveAttribute("readOnly");
      });
    });

    it("toggles enabled checkbox", async () => {
      const editButton = screen.getByTestId("edit-icon");
      await user.click(editButton);

      await waitFor(() => {
        const checkbox = screen.getByRole("checkbox", { name: "Enabled" });
        expect(checkbox).not.toBeDisabled();
      });

      const checkbox = screen.getByRole("checkbox", { name: "Enabled" });
      await user.click(checkbox);

      expect(checkbox).not.toBeChecked();
    });

    it("deletes SNMP group", async () => {
      const deleteButton = screen.getByTestId("trash-icon");
      await user.click(deleteButton);

      expect(screen.queryByText("Test Group 1")).not.toBeInTheDocument();
    });

    it("adds new SNMP group", async () => {
      const addButton = screen.getByText("+ Add SNMP Group");
      await user.click(addButton);

      const input = screen.getByPlaceholderText("Enter group name");
      await user.type(input, "New SNMP Group");

      const addGroupButton = screen.getByText("Add");
      await user.click(addGroupButton);

      expect(screen.getByText("New SNMP Group")).toBeInTheDocument();
    });

    it("renders correct input types for SNMP group fields", async () => {
      await user.click(screen.getByRole("button", { name: "SNMP Groups" }));

      await user.click(screen.getByTestId("chevron-down"));

      const snmpVersionInput = screen.getByDisplayValue("3");
      expect(snmpVersionInput).toHaveAttribute("type", "number");

      const authPasswordInput = screen.getByDisplayValue("testpass");
      expect(authPasswordInput).toHaveAttribute("type", "password");

      const groupNameInput = screen.getByDisplayValue("Test Group 1");
      expect(groupNameInput).toHaveAttribute("type", "text");
    });

    it("prevents editing when not in edit mode", async () => {
      const expandButton = screen.getByTestId("chevron-down");
      await user.click(expandButton);
      const input = screen.getByDisplayValue("Test Group 1");
      expect(input).toHaveAttribute("readOnly");
      await user.type(input, "New Name");
      expect(input).toHaveValue("Test Group 1");
    });

    it("allows editing snmp_secname as a string in SNMP group", async () => {
      const expandButton = screen.getByTestId("chevron-down");
      await user.click(expandButton);

      const editBtn = screen.getByTestId("edit-icon");
      await user.click(editBtn);

      const secnameInput = screen.getByDisplayValue("testuser");
      expect(secnameInput).not.toHaveAttribute("readOnly");

      await user.clear(secnameInput);
      await user.type(secnameInput, "newuser");
      expect(secnameInput).toHaveValue("newuser");
    });
  });

  // ---------- Advanced Tab ----------

  describe("Advanced Tab", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );

      await user.click(screen.getByRole("button", { name: "Advanced" }));
    });

    it("displays core and server sections", () => {
      expect(screen.getByText("Core")).toBeInTheDocument();
      expect(screen.getByText("Server")).toBeInTheDocument();
    });

    it("expands sections to show configuration fields", async () => {
      const coreSection = screen.getByText("Core").closest("details");
      const expandButton = within(coreSection!).getByTestId("chevron-down");

      await user.click(expandButton);

      expect(screen.getByDisplayValue("false")).toBeInTheDocument();
      expect(screen.getByDisplayValue("info")).toBeInTheDocument();
    });

    it("enters edit mode for sections", async () => {
      const coreSection = screen.getByText("Core").closest("details");
      const editButton = within(coreSection!).getByTestId("edit-icon");

      await user.click(editButton);

      await waitFor(() => {
        const debugInput = screen.getByDisplayValue("false");
        expect(debugInput).not.toHaveAttribute("readOnly");
      });
    });

    it("shows alert when password is incorrect", async () => {
      const promptSpy = vi.spyOn(window, "prompt").mockReturnValue("wrongpass");
      const alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});

      render(<ConfigPage />);
      const editButton = screen.getByTestId("password-edit-btn");
      await user.click(editButton);

      expect(alertSpy).toHaveBeenCalledWith("Incorrect password");

      promptSpy.mockRestore();
      alertSpy.mockRestore();
    });
    it("updates core section field when editing", async () => {
      const coreSection = screen.getByText("Core").closest("details");
      const editButton = within(coreSection!).getByTestId("edit-icon");
      await user.click(editButton);

      const debugInput = screen.getByDisplayValue("false");
      await user.clear(debugInput);
      await user.type(debugInput, "true");

      expect(debugInput).toHaveValue("true");
    });
  });

  // ---------- Save Functionality ----------

  describe("Save Functionality", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );
    });

    it("saves configuration successfully", async () => {
      mockFetch.mockImplementationOnce(
        () =>
          new Promise((resolve) =>
            setTimeout(() => resolve({ ok: true, json: async () => ({}) }), 50)
          )
      );

      const saveButton = screen.getByText("Save Configuration");
      await user.click(saveButton);

      expect(screen.getByText("Saving...")).toBeInTheDocument();
      await waitFor(() => {
        expect(screen.getByText("Saved!")).toBeInTheDocument();
      });
    });

    it("handles save error gracefully", async () => {
      // Mock failing fetch
      (fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({}),
      });

      const saveButton = screen.getByText("Save Configuration");
      await user.click(saveButton);

      await waitFor(() =>
        expect(screen.queryByText("Saving...")).not.toBeInTheDocument()
      );

      expect(screen.queryByText("Saved!")).not.toBeInTheDocument();
    });

    it("disables save button while saving", async () => {
      const neverResolvingFetch = new Promise<Response>(() => {});
      mockFetch.mockImplementationOnce(() => neverResolvingFetch);

      const saveButton = screen.getByText("Save Configuration");
      await user.click(saveButton);

      expect(saveButton).toBeDisabled();
      expect(saveButton).toHaveClass("cursor-not-allowed");
    });
  });

  // ---------- Accessibility ----------

  describe("Accessibility", () => {
    beforeEach(async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      render(<ConfigPage />);
      await waitFor(() =>
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument()
      );
    });

    it("has proper ARIA labels for buttons", () => {
      const editButtons = screen.getAllByLabelText(/edit/i);
      const deleteButtons = screen.getAllByLabelText(/delete/i);
      const expandButtons = screen.getAllByLabelText(/expand|collapse/i);

      expect(editButtons.length).toBeGreaterThan(0);
      expect(deleteButtons.length).toBeGreaterThan(0);
      expect(expandButtons.length).toBeGreaterThan(0);
    });

    it("has semantic HTML structure", () => {
      expect(screen.getByRole("navigation")).toBeInTheDocument();

      const buttons = screen.getAllByRole("button");
      expect(buttons.length).toBeGreaterThan(0);

      expect(screen.getByRole("banner")).toBeInTheDocument();
      expect(screen.getByRole("contentinfo")).toBeInTheDocument();
    });

    it("supports keyboard navigation", async () => {
      const firstTab = screen.getByRole("button", { name: "Zones" });
      firstTab.focus();

      await user.keyboard("{Tab}");
      expect(screen.getByRole("button", { name: "SNMP Groups" })).toHaveFocus();
    });
  });

  // ---------- Error Boundaries ----------

  describe("Error Boundaries", () => {
    it("handles missing config sections gracefully", async () => {
      const incompleteConfig = { poller: {} };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => incompleteConfig,
      });

      render(<ConfigPage />);

      await waitFor(() => {
        expect(screen.queryByText("Loading…")).not.toBeInTheDocument();
      });
      expect(screen.getByText("+ Add Zone")).toBeInTheDocument();
    });
  });
});

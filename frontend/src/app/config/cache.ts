// Type definitions
interface Zone {
  zone: string;
  hostnames: string[];
}
interface SNMPGroup {
  enabled: boolean;
  group_name: string;
  snmp_ip: string;
  snmp_version: number;
  snmp_secname: string;
  snmp_authprotocol: string;
  snmp_authpassword: string;
  snmp_privprotocol: string;
  snmp_privpassword: string;
  snmp_community: string;
}

interface PollerConfig {
  zones?: Zone[];
  snmp_groups?: SNMPGroup[];
}

interface Config {
  poller?: PollerConfig;
  core: Record<string, unknown>;
  server: Record<string, unknown>;
}

// Cache for config data
interface CacheEntry {
  data: Config;
  timestamp: number;
}
export let configCache: CacheEntry | null = null;

export const setConfigCache = (data: CacheEntry) => {
  configCache = data;
};

// This function is used only in tests to reset the config cache.
// Do not remove it even if it appears unused in the app.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const __resetConfigCache = (): void => {
  configCache = null;
};

export default configCache;

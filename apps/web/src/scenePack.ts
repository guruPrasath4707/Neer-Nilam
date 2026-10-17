export const SCENE_STATE_KINDS = [
  "DOCUMENTED",
  "RECONSTRUCTED",
  "INTERPRETED",
  "PROVISIONAL",
  "GAP",
] as const;

export type SceneStateKind = (typeof SCENE_STATE_KINDS)[number];

export interface ScenePack {
  scene_pack_version: string;
  scene_id: string;
  requested_interval: { from: string | null; to: string | null };
  resolved_state_id?: string | null;
  state_kind: SceneStateKind;
  entities: string[];
  layers: string[];
  events?: string[];
  evidence_refs?: string[];
  asset_refs?: string[];
  uncertainty?: { code?: string; message?: string; [key: string]: unknown } | null;
  attribution?: string[];
  rights_notices?: string[];
  data_gaps: string[];
  renderer_hints?: Record<string, unknown>;
  generated_at?: string | null;
  generator_version?: string | null;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === "string");
}

/**
 * Validate the essential scene-pack contract at the client boundary.
 * The repository's versioned JSON Schema remains the canonical full contract.
 */
export function parseScenePack(value: unknown): ScenePack {
  if (!isRecord(value)) {
    throw new Error("Scene pack must be a JSON object.");
  }

  if (typeof value.scene_pack_version !== "string" || value.scene_pack_version.length === 0) {
    throw new Error("Scene pack requires a non-empty scene_pack_version.");
  }

  if (typeof value.scene_id !== "string" || value.scene_id.length === 0) {
    throw new Error("Scene pack requires a non-empty scene_id.");
  }

  if (!isRecord(value.requested_interval)) {
    throw new Error("Scene pack requires a requested_interval object.");
  }

  for (const bound of ["from", "to"] as const) {
    const candidate = value.requested_interval[bound];
    if (candidate !== null && typeof candidate !== "string") {
      throw new Error("requested_interval." + bound + " must be a string or null.");
    }
  }

  if (
    typeof value.state_kind !== "string" ||
    !SCENE_STATE_KINDS.includes(value.state_kind as SceneStateKind)
  ) {
    throw new Error("Scene pack has an unsupported state_kind.");
  }

  if (!isStringArray(value.entities)) {
    throw new Error("Scene pack entities must be an array of strings.");
  }

  if (!isStringArray(value.layers)) {
    throw new Error("Scene pack layers must be an array of strings.");
  }

  if (!isStringArray(value.data_gaps)) {
    throw new Error("Scene pack data_gaps must be an array of strings.");
  }

  for (const field of ["events", "evidence_refs", "asset_refs", "attribution", "rights_notices"] as const) {
    if (value[field] !== undefined && !isStringArray(value[field])) {
      throw new Error("Scene pack " + field + " must be an array of strings when present.");
    }
  }

  return value as unknown as ScenePack;
}

export function isGapScenePack(scenePack: ScenePack): boolean {
  return scenePack.state_kind === "GAP";
}

export function gapExplanation(scenePack: ScenePack): string {
  if (!isGapScenePack(scenePack)) {
    return "This scene pack has a non-GAP state. Its evidence and rights still require normal review.";
  }

  const message = scenePack.uncertainty?.message;
  if (typeof message === "string" && message.trim().length > 0) {
    return message;
  }

  return "No supported historical reconstruction is registered for this scene pack. The client will not substitute an unverified historical state.";
}

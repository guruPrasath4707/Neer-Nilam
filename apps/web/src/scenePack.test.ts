import { describe, expect, it } from "vitest";
import gapScenePack from "../../../data/scene-packs/BRH-001-GAP-FIXTURE.json";
import { gapExplanation, isGapScenePack, parseScenePack } from "./scenePack";

describe("Neer-Nilam scene-pack boundary", () => {
  it("accepts the current Brihadisvara GAP fixture", () => {
    const scenePack = parseScenePack(gapScenePack as unknown);
    expect(scenePack.scene_id).toBe("BRH-001-GAP-FIXTURE");
    expect(scenePack.state_kind).toBe("GAP");
    expect(scenePack.data_gaps).toContain("NN:state:brihadisvara:gap-001");
  });

  it("renders unsupported history as an explicit gap", () => {
    const scenePack = parseScenePack(gapScenePack as unknown);
    expect(isGapScenePack(scenePack)).toBe(true);
    expect(gapExplanation(scenePack)).toContain("will not substitute an unverified historical state");
  });

  it("rejects a scene pack that is not an object", () => {
    expect(() => parseScenePack(null)).toThrow("JSON object");
  });

  it("rejects an unsupported historical state kind", () => {
    const invalid = { ...gapScenePack, state_kind: "INVENTED" };
    expect(() => parseScenePack(invalid as unknown)).toThrow("unsupported state_kind");
  });

  it("rejects missing required data-gap metadata", () => {
    const invalid = { ...gapScenePack, data_gaps: undefined };
    expect(() => parseScenePack(invalid as unknown)).toThrow("data_gaps");
  });
});

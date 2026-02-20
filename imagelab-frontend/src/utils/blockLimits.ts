import * as Blockly from "blockly";

export const SINGLETON_BLOCK_TYPES = new Set(["basic_readimage", "basic_writeimage"]);

export function isSingletonBlockPresent(workspace: Blockly.WorkspaceSvg, type: string): boolean {
  return workspace.getBlocksByType(type).length > 0;
}

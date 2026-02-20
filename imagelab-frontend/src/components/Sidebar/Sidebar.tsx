import { useState, useEffect, useMemo } from "react";
import * as Blockly from "blockly";
import { categories } from "../../blocks/categories";
import { useBlockPreviews } from "../../hooks/useBlockPreviews";
import { SINGLETON_BLOCK_TYPES } from "../../utils/blockLimits";
import CategorySection from "./CategorySection";

interface SidebarProps {
  workspace: Blockly.WorkspaceSvg | null;
}

export default function Sidebar({ workspace }: SidebarProps) {
  const previews = useBlockPreviews();
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (!workspace) return;
    const listener = (event: Blockly.Events.Abstract) => {
      if (
        event.type === Blockly.Events.BLOCK_CREATE ||
        event.type === Blockly.Events.BLOCK_DELETE
      ) {
        setTick((t) => t + 1);
      }
    };
    workspace.addChangeListener(listener);
    return () => workspace.removeChangeListener(listener);
  }, [workspace]);

  const presentSingletons = useMemo(() => {
    if (!workspace) return new Set<string>();
    const present = new Set<string>();
    for (const type of SINGLETON_BLOCK_TYPES) {
      if (workspace.getBlocksByType(type).length > 0) {
        present.add(type);
      }
    }
    return present;
    // eslint-disable-next-line react-hooks/exhaustive-deps -- tick triggers recomputation on block create/delete
  }, [workspace, tick]);

  return (
    <div className="w-80 h-full bg-white border-r border-gray-200 overflow-y-auto flex-shrink-0">
      <div className="px-3 py-2 border-b border-gray-200">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Blocks</h2>
      </div>
      {categories.map((category) => (
        <CategorySection
          key={category.name}
          category={category}
          workspace={workspace}
          previews={previews}
          disabledTypes={presentSingletons}
          defaultOpen={category.name === "Basic"}
        />
      ))}
    </div>
  );
}

import { create } from 'zustand';

interface PipelineState {
  originalImage: string | null;
  imageFormat: string;
  processedImage: string | null;
  isExecuting: boolean;
  error: string | null;
  errorStep: number | null;
  selectedBlockType: string | null;
  selectedBlockTooltip: string | null;
  setOriginalImage: (image: string, format: string) => void;
  setProcessedImage: (image: string | null) => void;
  setExecuting: (executing: boolean) => void;
  setError: (error: string | null, step?: number | null) => void;
  setSelectedBlock: (type: string | null, tooltip: string | null) => void;
  reset: () => void;
  clearImage: () => void;
  _imageResetFn: (() => void) | null;
  registerImageReset: (fn: () => void) => void;
}

export const usePipelineStore = create<PipelineState>((set) => ({
  originalImage: null,
  imageFormat: 'png',
  processedImage: null,
  isExecuting: false,
  error: null,
  errorStep: null,
  selectedBlockType: null,
  selectedBlockTooltip: null,
  setOriginalImage: (image, format) => set({ originalImage: image, imageFormat: format, processedImage: null, error: null }),
  setProcessedImage: (image) => set({ processedImage: image, error: null, errorStep: null }),
  setExecuting: (executing) => set({ isExecuting: executing }),
  setError: (error, step = null) => set({ error, errorStep: step }),
  setSelectedBlock: (type, tooltip) => set({ selectedBlockType: type, selectedBlockTooltip: tooltip }),
  reset: () => set({ originalImage: null, imageFormat: 'png', processedImage: null, isExecuting: false, error: null, errorStep: null, selectedBlockType: null, selectedBlockTooltip: null }),
  _imageResetFn: null as (() => void) | null,
  registerImageReset: (fn) => set({ _imageResetFn: fn }),
  clearImage: () => {
    const state = usePipelineStore.getState();
    if (state._imageResetFn) state._imageResetFn();
    set({ originalImage: null, processedImage: null, error: null, errorStep: null });
  },

}));

import { createSharedComposable, useBreakpoints } from '@vueuse/core';

export const useBreakpointQuery = createSharedComposable(() => {
  const breakpoints = useBreakpoints({
    pc: 1024,
  });

  const isMobile = breakpoints.smaller('pc');
  const isPC = breakpoints.isGreater('pc');

  return {
    breakpoints,
    isMobile,
    isPC,
  };
});

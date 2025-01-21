export const useProgramStore = defineStore('program', () => {
  const { execute: start } = useApi(apiProgram.start);
  const { execute: pause } = useApi(apiProgram.stop);
  const { execute: shutdown } = useApi(apiProgram.shutdown);
  const { execute: restart } = useApi(apiProgram.restart);
  const { execute: resetRule } = useApi(apiBangumi.resetAll);

  return {
    start,
    pause,
    shutdown,
    restart,
    resetRule,
  };
});

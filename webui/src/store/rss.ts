import type { RSS } from '#/rss';

export const useRSSStore = defineStore('rss', () => {
  const rss = ref<RSS[]>([]);
  const selectedRSS = ref<number[]>([]);

  async function getAll() {
    const res = await apiRSS.get();

    function sort(arr: RSS[]) {
      return arr.sort((a, b) => b.id - a.id);
    }

    const enabled = sort(res.filter((e) => e.enabled));
    const disabled = sort(res.filter((e) => !e.enabled));

    rss.value = [...enabled, ...disabled];
  }

  const opts = {
    showMessage: true,
    onSuccess() {
      getAll();
      selectedRSS.value = [];
    },
  };

  const { execute: updateRSS } = useApi(apiRSS.update, opts);
  const { execute: disableRSS } = useApi(apiRSS.disableMany, opts);
  const { execute: deleteRSS } = useApi(apiRSS.deleteMany, opts);
  const { execute: enableRSS } = useApi(apiRSS.enableMany, opts);

  const disableSelected = () => disableRSS(selectedRSS.value);
  const deleteSelected = () => deleteRSS(selectedRSS.value);
  const enableSelected = () => enableRSS(selectedRSS.value);

  return {
    rss,
    selectedRSS,

    getAll,
    updateRSS,
    disableRSS,
    deleteRSS,
    enableRSS,
    disableSelected,
    deleteSelected,
    enableSelected,
  };
});

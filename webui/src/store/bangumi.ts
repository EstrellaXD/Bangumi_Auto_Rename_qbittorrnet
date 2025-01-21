import type { BangumiRule } from '#/bangumi';
import { ruleTemplate } from '#/bangumi';

export const useBangumiStore = defineStore('bangumi', () => {
  const bangumi = ref<BangumiRule[]>();
  const editRule = reactive<{
    show: boolean;
    item: BangumiRule;
  }>({
    show: false,
    item: ruleTemplate,
  });

  async function getAll() {
    const res = await apiBangumi.getAll();
    const sort = (arr: BangumiRule[]) => arr.sort((a, b) => b.id - a.id);

    const enabled = sort(res.filter((e) => !e.deleted));
    const disabled = sort(res.filter((e) => e.deleted));

    bangumi.value = [...enabled, ...disabled];
  }

  function refreshData() {
    editRule.show = false;
    getAll();
  }

  const opts = {
    showMessage: true,
    onSuccess() {
      refreshData();
    },
  };

  const { execute: updateRule } = useApi(apiBangumi.updateRule, opts);
  const { execute: enableRule } = useApi(apiBangumi.enableRule, opts);
  const { execute: disableRule } = useApi(apiBangumi.disableRule, opts);
  const { execute: deleteRule } = useApi(apiBangumi.deleteRule, opts);
  const { execute: refreshPoster } = useApi(apiBangumi.refreshPoster, opts);

  function openEditPopup(data: BangumiRule) {
    editRule.show = true;
    editRule.item = data;
  }

  function ruleManage(
    type: 'disable' | 'delete',
    id: number,
    deleteFile: boolean
  ) {
    switch (type) {
      case 'disable':
        disableRule(id, deleteFile);
        break;

      case 'delete':
        deleteRule(id, deleteFile);
        break;
    }
  }

  return {
    bangumi,
    editRule,

    getAll,
    updateRule,
    enableRule,
    disableRule,
    deleteRule,
    refreshPoster,
    openEditPopup,
    ruleManage,
  };
});

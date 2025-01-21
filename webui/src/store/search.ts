import { ref } from 'vue';
import { EMPTY, Subject, debounceTime, switchMap, tap } from 'rxjs';
import type { BangumiRule, SearchResult } from '#/bangumi';

export const useSearchStore = defineStore('search', () => {
  const bangumiList = ref<SearchResult[]>([]);
  const inputValue = ref<string>('');

  const providers = ref<string[]>(['mikan', 'dmhy', 'nyaa']);
  const provider = ref<string>(providers.value[0]);

  const loading = ref<boolean>(false);

  const input$ = new Subject<string>();

  watch(inputValue, (input) => {
    input$.next(input);
    loading.value = !!input;
  });

  function getProviders() {
    apiSearch.getProvider().then((res) => {
      providers.value = res;
    });
  }

  /**
   * - 输入中 debounce 600ms 后触发搜索
   * - 按回车或点击搜索 icon 按钮后触发搜索
   * - 切换 provider 源站时触发搜索
   */

  const bangumiInfo$ = input$
    .pipe(
      debounceTime(600),
      // switchMap 把输入 keyword 查询为 bangumiInfo$ 流，多次输入自动取消并停止前一次查询
      switchMap((input: string) => {
        // 有输入更新后清理之前的搜索结果
        bangumiList.value = [];
        return input ? apiSearch.get(input, provider.value) : EMPTY;
      }),
      tap((bangumi: BangumiRule) => {
        const result: SearchResult = {
          order: bangumiList.value.length + 1,
          value: bangumi,
        };
        bangumiList.value.push(result);
      })
    )
    .subscribe();

  function onSearch() {
    input$.next(inputValue.value);
  }

  function clearSearch() {
    inputValue.value = '';
    bangumiList.value = [];
  }

  return {
    input$,
    bangumiInfo$,
    inputValue,
    loading,
    provider,
    providers,
    bangumiList,

    onSearch,
    clearSearch,
    getProviders,
  };
});

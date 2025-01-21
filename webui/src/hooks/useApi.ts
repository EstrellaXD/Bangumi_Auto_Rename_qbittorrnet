type AnyAsyncFuntion<TData = any> = (...args: any[]) => Promise<TData>;

interface Options<T = any> {
  showMessage?: boolean;
  onBeforeExecute?: () => void;
  onSuccess?: (data: T) => void;
  onError?: (error: any) => void;
  onFinally?: () => void;
}

export function useApi<
  TApi extends AnyAsyncFuntion = AnyAsyncFuntion,
  TData = Awaited<ReturnType<TApi>>
>(
  api: TApi,
  {
    showMessage = true,
    onBeforeExecute,
    onSuccess,
    onError,
    onFinally,
  }: Options = {}
) {
  const data = ref<TData>();
  const isLoading = ref(false);

  const message = useMessage();
  const { returnUserLangMsg } = useMyI18n();

  async function execute(...params: Parameters<TApi>) {
    onBeforeExecute?.();

    try {
      isLoading.value = true;
      const res = await api(...params);
      data.value = res;

      onSuccess?.(res);

      if (showMessage && 'msg_en' in res) {
        message.success(returnUserLangMsg(res));
      }
    } catch (err) {
      onError?.(err);
    } finally {
      isLoading.value = false;
      onFinally?.();
    }
  }

  return {
    data,
    isLoading,

    execute,
  };
}

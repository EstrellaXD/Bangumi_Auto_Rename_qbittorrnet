<script lang="ts" setup>
definePage({
  name: 'Log',
});

const { onUpdate, offUpdate, reset, copy, getLog } = useLogStore();
const { log } = storeToRefs(useLogStore());
const { version } = useAppInfo();

const formatLog = computed(() => {
  const list = log.value
    .trim()
    .split('\n')
    .filter((i) => i !== '');
  const startIndex = list.findIndex((i) => /Version/.test(i));

  return list.slice(startIndex === -1 ? 0 : startIndex).map((i, index) => {
    const date = i.match(/\[\d+-\d+-\d+\ \d+:\d+:\d+\]/)?.[0] || '';
    const type = i.match(/(INFO)|(WARNING)|(ERROR)|(DEBUG)/)?.[0] || '';
    const content = i.replace(date, '').replace(`${type}:`, '').trim();

    return {
      index,
      date,
      type,
      content,
    };
  });
});

function typeColor(type: string) {
  const M = {
    INFO: '#4e3c94',
    WARNING: '#A76E18',
    ERROR: '#C70E0E',
    DEBUG: '#A0A0A0',
  };
  return M[type];
}

const logContainer = ref<HTMLElement | null>(null);

function backToBottom() {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight;
  }
}

onActivated(() => {
  onUpdate();

  if (log.value) {
    backToBottom();
  } else {
    watchOnce(log, () => {
      nextTick(() => {
        backToBottom();
      });
    });
  }
});

onDeactivated(() => {
  offUpdate();
});
</script>

<template>
  <div overflow-auto mt-12 flex-grow>
    <div flex="~ wrap gap-12">
      <ab-container :title="$t('log.title')" w-660 grow>
        <div
          ref="logContainer"
          rounded-10
          border="1 solid black"
          overflow-auto
          p-10
          max-h-60vh
          min-h-20vh
        >
          <div min-w-450>
            <template v-for="i in formatLog" :key="i.index">
              <div
                p="y-10"
                leading="1.5em"
                border="0 b-1 solid"
                last:border-b-0
                flex="~ items-center gap-20"
                :style="{ color: typeColor(i.type) }"
              >
                <div flex="~ col items-center gap-10" whitespace-nowrap>
                  <div text="center">{{ i.type }}</div>
                  <div>{{ i.date }}</div>
                </div>

                <div flex-1 break-all>{{ i.content }}</div>
              </div>
            </template>
          </div>
        </div>

        <div flex="~ justify-end gap-x-10" mt-12>
          <ab-button size="small" @click="getLog">
            {{ $t('log.update_now') }}
          </ab-button>

          <ab-button type="warn" size="small" @click="reset">
            {{ $t('log.reset') }}
          </ab-button>

          <ab-button size="small" @click="copy">
            {{ $t('log.copy') }}
          </ab-button>
        </div>
      </ab-container>

      <div grow w-500 space-y-20>
        <ab-container :title="$t('log.contact_info')">
          <div space-y-12>
            <ab-label label="Github">
              <ab-button
                size="small"
                link="https://github.com/EstrellaXD/Auto_Bangumi"
                target="_blank"
              >
                {{ $t('log.go') }}
              </ab-button>
            </ab-label>

            <ab-label label="Official Website">
              <ab-button
                size="small"
                link="https://autobangumi.org"
                target="_blank"
              >
                {{ $t('log.go') }}
              </ab-button>
            </ab-label>

            <div line></div>

            <ab-label label="X">
              <ab-button
                size="small"
                link="https://twitter.com/Estrella_Pan"
                target="_blank"
              >
                {{ $t('log.go') }}
              </ab-button>
            </ab-label>

            <ab-label label="Telegram Group">
              <ab-button
                size="small"
                link="https://t.me/autobangumi"
                target="_blank"
              >
                {{ $t('log.join') }}
              </ab-button>
            </ab-label>
          </div>
        </ab-container>

        <ab-container :title="$t('log.bug_repo')">
          <div space-y-12>
            <ab-button
              mx-auto
              text-16
              w-300
              h-46
              rounded-10
              link="https://github.com/EstrellaXD/Auto_Bangumi/issues"
            >
              Github Issues
            </ab-button>

            <div line></div>

            <div text="center primary h3">
              <span>Version: </span>
              <span>{{ version }}</span>
            </div>
          </div>
        </ab-container>
      </div>
    </div>
  </div>
</template>

<script lang="tsx" setup>
import {
  Calendar,
  Download,
  Home,
  Log,
  Logout,
  MenuUnfold,
  Play,
  SettingTwo,
} from '@icon-park/vue-next';
import InlineSvg from 'vue-inline-svg';

const props = withDefaults(
  defineProps<{
    open?: boolean;
  }>(),
  {
    open: false,
  }
);

const { t } = useMyI18n();
const { logout } = useAuth();
const route = useRoute();
const { isMobile } = useBreakpointQuery();

const show = ref(props.open);
const toggle = () => (show.value = !show.value);

const RSS = h(
  'span',
  { class: ['rel', 'left-2'] },
  h(InlineSvg, { src: './images/RSS.svg' })
);

const items = [
  {
    id: 1,
    icon: Home,
    label: () => t('sidebar.homepage'),
    path: '/bangumi',
  },
  {
    id: 2,
    icon: Calendar,
    label: () => t('sidebar.calendar'),
    path: '/calendar',
    hidden: true,
  },
  {
    id: 3,
    icon: RSS,
    label: () => t('sidebar.rss'),
    path: '/rss',
  },
  {
    id: 4,
    icon: Play,
    label: () => t('sidebar.player'),
    path: '/player',
  },
  {
    id: 5,
    icon: Download,
    label: () => t('sidebar.downloader'),
    path: '/downloader',
    hidden: localStorage.getItem('enable_downloader_iframe') !== '1',
  },
  {
    id: 6,
    icon: Log,
    label: () => t('sidebar.log'),
    path: '/log',
  },
  {
    id: 7,
    icon: SettingTwo,
    label: () => t('sidebar.config'),
    path: '/config',
  },
];

function Exit() {
  return (
    <div
      title="logout"
      class={[
        `
        mt-auto
        fx-cer
        gap-x-42
        px-24
        is-btn
        transition-colors
      `,
        isMobile.value ? 'h-40' : 'h-48',
      ]}
      hover="bg-[#F1F5FA] text-[#2A1C52]"
      onClick={logout}
    >
      <Logout size={24} />
      {!isMobile.value && <div class="text-h2">{t('sidebar.logout')}</div>}
    </div>
  );
}

const mobileItems = computed(() => items.filter((i) => i.id !== 4));
</script>

<template>
  <media-query>
    <div
      :class="[show ? 'w-240' : 'w-72']"
      bg-theme-col
      text-white
      transition-width
      pb-12
      rounded="pc:16 10"
    >
      <div overflow-hidden wh-full flex="~ col">
        <div
          w-full
          h-60
          is-btn
          f-cer
          rounded-t-10
          bg="#E7E7E7"
          text="#2A1C52"
          rel
          @click="toggle"
        >
          <div :class="[!show && 'abs opacity-0']" transition-opacity>
            <div text-h1>{{ $t('sidebar.title') }}</div>
          </div>

          <MenuUnfold
            theme="outline"
            size="24"
            fill="#2A1C52"
            abs
            left-24
            :class="[show && 'rotate-y-180']"
          />
        </div>

        <RouterLink
          v-for="i in items"
          :key="i.id"
          :to="i.path"
          replace
          :title="i.label()"
          fx-cer
          px-24
          gap-x-42
          h-48
          is-btn
          transition-colors
          hover="bg-[#F1F5FA] text-[#2A1C52]"
          :class="[
            route.path === i.path && 'bg-[#F1F5FA] text-[#2A1C52]',
            i.hidden && 'hidden',
          ]"
        >
          <Component :is="i.icon" :size="24" />

          <div text-h2 whitespace-nowrap>{{ i.label() }}</div>
        </RouterLink>

        <Exit />
      </div>
    </div>

    <template #mobile>
      <div bg-white flex rounded-10 overflow-hidden>
        <RouterLink
          v-for="i in mobileItems"
          :key="i.id"
          :to="i.path"
          replace
          flex-1
          fx-cer
          px-24
          gap-x-42
          h-40
          is-btn
          transition-colors
          rounded-10
          :class="[
            route.path === i.path && 'bg-theme-row text-white',
            i.hidden && 'hidden',
          ]"
        >
          <Component :is="i.icon" :size="24" />
        </RouterLink>

        <Exit />
      </div>
    </template>
  </media-query>
</template>

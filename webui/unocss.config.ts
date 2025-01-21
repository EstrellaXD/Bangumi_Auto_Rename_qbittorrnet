import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetUno,
} from 'unocss';
import presetRemToPx from '@unocss/preset-rem-to-px';

export default defineConfig({
  presets: [
    presetUno(),
    presetRemToPx({
      baseFontSize: 4,
    }),
    presetAttributify(),
    presetIcons({ cdn: 'https://esm.sh/' }),
  ],
  preflights: [
    {
      getCSS: () => `
        :root {
          font-size: 4px;
        }
        body {
          font-size: 4rem;
        }
      `,
    },
  ],
  theme: {
    breakpoints: {
      pc: '1024px',
    },
    colors: {
      primary: '#493475',
      running: '#A3D491',
      stopped: '#DF7F91',
      page: '#F0F0F0',
    },
  },
  rules: [
    [
      'bg-theme-row',
      {
        background: 'linear-gradient(90.5deg, #492897 1.53%, #783674 96.48%)',
      },
    ],
    [
      'bg-theme-col',
      {
        background: 'linear-gradient(180deg, #492897 0%, #783674 100%)',
      },
    ],
    [
      'poster-shandow',
      {
        filter: 'drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.1))',
      },
    ],
    [
      'poster-pen-active',
      {
        background: '#B4ABC6',
        'box-shadow': '2px 2px 4px rgba(0, 0, 0, 0.25)',
      },
    ],
  ],
  shortcuts: [
    [/^wh-(.*)$/, ([, t]) => `w-${t} h-${t}`],
    [/^text-limit-(\d{0,})$/, ([, n]) => `line-clamp-${n}`],

    // position
    {
      rel: 'relative',
      abs: 'absolute',
    },

    // flex
    {
      'fx-cer': 'flex items-center',
      'f-cer': 'flex items-center justify-center',
    },

    // font size
    {
      'text-h1': 'text-24',
      'text-h2': 'text-20',
      'text-h3': 'text-16',
      'text-main': 'text-12',
    },

    // input
    {
      'ab-input': `outline-none min-w-0 w-200 h-28
                     px-12 text-main text-right
                     rounded-6 shadow-inset
                     border-1 border-black hover:border-color-[#7A46AE]
                    `,

      'input-error': 'border-color-[#CA0E0E]',
      'input-reset': 'bg-transparent min-w-0 flex-1 outline-none',
    },

    // status
    {
      'is-btn': 'cursor-pointer select-none',
      'btn-click': 'hover:scale-110 active:scale-100',
      'is-disabled': 'cursor-not-allowed select-none',
    },

    // other
    {
      line: 'w-full h-1 bg-[#DFE1EF]',
    },
  ],
});

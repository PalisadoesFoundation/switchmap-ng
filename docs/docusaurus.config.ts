import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: "Switchmap-NG",
  tagline: "Inventory, Status & Visualization of Your Network Devices.",
  favicon: 'img/logo/switchmap-logo-modified.svg',

  url: "https://docs.switchmap-ng.io/",
  baseUrl: '/',
  deploymentBranch: "gh-pages",

  organizationName: "PalisadoesFoundation", // GitHub org
  projectName: "switchmap-ng", // repo name

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn', // Or 'throw', 'ignore'
    },
  },
  
  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/PalisadoesFoundation/switchmap-ng/tree/develop/docs/',
          exclude: ['**/node_modules/**'],
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    docs: {
      sidebar: {
        hideable: false,
      },
    },
    navbar: {
      title: "Switchmap-NG",
      logo: {
        alt: "SwitchMap-NG logo",
        src: "img/logo/switchmap-logo-modified.svg",
        className: "LogoAnimation",
      },
      items: [
        {
          label: "Docs",
          position: "left",
          to: "/docs",
          target: "_self",
        },
        
        {
          to: "https://github.com/PalisadoesFoundation",
          position: "right",
          className: "header-github-link",
          "aria-label": "GitHub repository",
        },
        
        {
          to: "https://www.youtube.com/@PalisadoesOrganization",
          position: "right",
          className: "header-youtube-link",
          "aria-label": "Palisadoes Youtube channel",
        },
      ],
    },
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Community",
          items: [
            {
              label: " Slack",
              to: "https://github.com/PalisadoesFoundation",
              className: "footer__icon footer__slack",
            },
            {
              label: " News",
              to: "https://www.palisadoes.org/news/",
              className: "footer__icon footer__news",
            },
            {
              label: " Contact Us",
              to: "https://www.palisadoes.org/contact/",
              className: "footer__icon footer__contact",
            },
          ],
        },
        {
          title: "Social Media",
          items: [
            {
              label: " Twitter",
              to: "https://twitter.com/palisadoesorg?lang=en",
              className: "footer__icon footer__twitter",
            },
            {
              label: " Facebook",
              to: "https://www.facebook.com/palisadoesproject/",
              className: "footer__icon footer__facebook",
            },
            {
              label: " Instagram",
              to: "https://www.instagram.com/palisadoes/?hl=en",
              className: "footer__icon footer__instagram",
            },
          ],
        },
        {
          title: "Development",
          items: [
            {
              label: " GitHub",
              to: "https://github.com/PalisadoesFoundation",
              className: "footer__icon footer__github",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} The Palisadoes Foundation, LLC. Built with Docusaurus.`,
    },
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },         
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;

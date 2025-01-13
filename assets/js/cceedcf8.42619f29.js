"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[194],{9946:(e,s,a)=>{a.r(s),a.d(s,{assets:()=>o,contentTitle:()=>c,default:()=>h,frontMatter:()=>i,metadata:()=>n,toc:()=>l});const n=JSON.parse('{"id":"operation","title":"Operation","description":"The switchmap-ng CLI is meant for ease of use. This page shows some","source":"@site/docs/operation.md","sourceDirName":".","slug":"/operation","permalink":"/docs/operation","draft":false,"unlisted":false,"editUrl":"https://github.com/PalisadoesFoundation/switchmap-ng/blob/main/docs/docs/operation.md","tags":[],"version":"current","sidebarPosition":5,"frontMatter":{"title":"Operation","sidebar_label":"Operation","sidebar_position":5},"sidebar":"tutorialSidebar","previous":{"title":"CLI","permalink":"/docs/cli"},"next":{"title":"Webserver","permalink":"/docs/webserver"}}');var t=a(4848),r=a(8453);const i={title:"Operation",sidebar_label:"Operation",sidebar_position:5},c="Advanced Operation",o={},l=[{value:"Running Switchmap Processes as System Daemons",id:"running-switchmap-processes-as-system-daemons",level:2},{value:"Operating the Poller as a System Daemon",id:"operating-the-poller-as-a-system-daemon",level:3},{value:"Operating the API server as a System Daemon",id:"operating-the-api-server-as-a-system-daemon",level:3},{value:"Operating the Ingester as a System Daemon",id:"operating-the-ingester-as-a-system-daemon",level:3},{value:"Operating the Dashboard as a System Daemon",id:"operating-the-dashboard-as-a-system-daemon",level:3}];function d(e){const s={code:"code",h1:"h1",h2:"h2",h3:"h3",header:"header",li:"li",ol:"ol",p:"p",pre:"pre",...(0,r.R)(),...e.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(s.header,{children:(0,t.jsx)(s.h1,{id:"advanced-operation",children:"Advanced Operation"})}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"switchmap-ng"})," CLI is meant for ease of use. This page shows some\nadvanced features."]}),"\n",(0,t.jsx)(s.h2,{id:"running-switchmap-processes-as-system-daemons",children:"Running Switchmap Processes as System Daemons"}),"\n",(0,t.jsx)(s.p,{children:"All the switchmap daemon executables can be configured to run at the\nsystem level using systemd. This means that they will reliably restart\nafter a reboot. This is therefore the preferred mode of operation for\nproduction systems."}),"\n",(0,t.jsxs)(s.ol,{children:["\n",(0,t.jsxs)(s.li,{children:["Sample ",(0,t.jsx)(s.code,{children:"systemd"})," files can be found in the ",(0,t.jsx)(s.code,{children:"examples/linux/systemd/"}),"\ndirectory."]}),"\n",(0,t.jsx)(s.li,{children:"Each file contains instructions as to what to do"}),"\n"]}),"\n",(0,t.jsx)(s.h3,{id:"operating-the-poller-as-a-system-daemon",children:"Operating the Poller as a System Daemon"}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"poller"})," can be started like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl start switchmap_poller.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"poller"})," can be stopped like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl stop switchmap_poller.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the status of the ",(0,t.jsx)(s.code,{children:"poller"})," like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl status switchmap_poller.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the ",(0,t.jsx)(s.code,{children:"poller"})," to automatically restart on boot like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl enable switchmap_poller.service\n"})}),"\n",(0,t.jsx)(s.h3,{id:"operating-the-api-server-as-a-system-daemon",children:"Operating the API server as a System Daemon"}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"server"})," can be started like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl start switchmap_server.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"server"})," can be stopped like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl stop switchmap_server.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the status of the ",(0,t.jsx)(s.code,{children:"server"})," like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl status switchmap_server.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the ",(0,t.jsx)(s.code,{children:"server"})," to automatically restart on boot like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl enable switchmap_server.service\n"})}),"\n",(0,t.jsx)(s.h3,{id:"operating-the-ingester-as-a-system-daemon",children:"Operating the Ingester as a System Daemon"}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"ingester"})," can be started like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl start switchmap_ingester.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"ingester"})," can be stopped like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl stop switchmap_ingester.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the status of the ",(0,t.jsx)(s.code,{children:"ingester"})," like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl status switchmap_ingester.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the ",(0,t.jsx)(s.code,{children:"ingester"})," to automatically restart on boot like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl enable switchmap_ingester.service\n"})}),"\n",(0,t.jsx)(s.h3,{id:"operating-the-dashboard-as-a-system-daemon",children:"Operating the Dashboard as a System Daemon"}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"dashboard"})," can be started like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl start switchmap_dashboard.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["The ",(0,t.jsx)(s.code,{children:"dashboard"})," can be stopped like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl stop switchmap_dashboard.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the status of the ",(0,t.jsx)(s.code,{children:"dashboard"})," like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl status switchmap_dashboard.service\n"})}),"\n",(0,t.jsxs)(s.p,{children:["You can get the ",(0,t.jsx)(s.code,{children:"dashboard"})," to automatically restart on boot like this:"]}),"\n",(0,t.jsx)(s.pre,{children:(0,t.jsx)(s.code,{className:"language-bash",children:"$ sudo systemctl enable switchmap_dashboard.service\n"})})]})}function h(e={}){const{wrapper:s}={...(0,r.R)(),...e.components};return s?(0,t.jsx)(s,{...e,children:(0,t.jsx)(d,{...e})}):d(e)}},8453:(e,s,a)=>{a.d(s,{R:()=>i,x:()=>c});var n=a(6540);const t={},r=n.createContext(t);function i(e){const s=n.useContext(r);return n.useMemo((function(){return"function"==typeof e?e(s):{...s,...e}}),[s,e])}function c(e){let s;return s=e.disableParentContext?"function"==typeof e.components?e.components(t):e.components||t:i(e.components),n.createElement(r.Provider,{value:s},e.children)}}}]);
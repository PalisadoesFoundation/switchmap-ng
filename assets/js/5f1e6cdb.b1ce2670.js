"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[419],{6001:(e,n,s)=>{s.r(n),s.d(n,{assets:()=>a,contentTitle:()=>o,default:()=>d,frontMatter:()=>r,metadata:()=>t,toc:()=>l});const t=JSON.parse('{"id":"webserver","title":"Webserver","description":"You can access switchmap-ng on its default port 7000, however you may","source":"@site/docs/webserver.md","sourceDirName":".","slug":"/webserver","permalink":"/docs/webserver","draft":false,"unlisted":false,"editUrl":"https://github.com/PalisadoesFoundation/switchmap-ng/blob/main/docs/docs/webserver.md","tags":[],"version":"current","sidebarPosition":6,"frontMatter":{"title":"Webserver","sidebar_label":"Webserver","sidebar_position":6},"sidebar":"tutorialSidebar","previous":{"title":"Operation","permalink":"/docs/operation"},"next":{"title":"Testing","permalink":"/docs/testing"}}');var c=s(4848),i=s(8453);const r={title:"Webserver",sidebar_label:"Webserver",sidebar_position:6},o="Webserver Setup",a={},l=[{value:"Apache setup for <code>switchmap-ng</code>",id:"apache-setup-for-switchmap-ng",level:2},{value:"Nginx setup for <code>switchmap-ng</code>",id:"nginx-setup-for-switchmap-ng",level:2}];function h(e){const n={code:"code",h1:"h1",h2:"h2",header:"header",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,i.R)(),...e.components};return(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(n.header,{children:(0,c.jsx)(n.h1,{id:"webserver-setup",children:"Webserver Setup"})}),"\n",(0,c.jsxs)(n.p,{children:["You can access ",(0,c.jsx)(n.code,{children:"switchmap-ng"})," on its default port 7000, however you may\nwant to access it on port 80 by integrating it with an Apache or Nginx\nwebserver. This page explains how."]}),"\n",(0,c.jsxs)(n.h2,{id:"apache-setup-for-switchmap-ng",children:["Apache setup for ",(0,c.jsx)(n.code,{children:"switchmap-ng"})]}),"\n",(0,c.jsxs)(n.p,{children:[(0,c.jsx)(n.code,{children:"switchmap-ng"})," has sample configurations for the Apache webserver."]}),"\n",(0,c.jsxs)(n.p,{children:["Run the following commands from the top directory of ",(0,c.jsx)(n.code,{children:"switchmap-ng"})]}),"\n",(0,c.jsx)(n.pre,{children:(0,c.jsx)(n.code,{children:"$ sudo cp examples/linux/apache/switchmap-ng-apache.conf /etc/apache2/conf-available\n$ sudo ln -s /etc/apache2/conf-available/switchmap-ng-apache.conf /etc/apache2/conf-enabled/switchmap-ng-apache.conf \n\n# (Ubuntu only)\n$ sudo a2enmod proxy_http\n$ sudo systemctl restart apache2.service\n\n# (RedHat / CentOS)    \n$ sudo systemctl restart httpd.service\n"})}),"\n",(0,c.jsxs)(n.p,{children:["You should now be able to access your ",(0,c.jsx)(n.code,{children:"switchmap-ng"})," web pages using the\nfollowing link."]}),"\n",(0,c.jsxs)(n.ul,{children:["\n",(0,c.jsx)(n.li,{children:"http://SERVER_NAME/switchmap/"}),"\n"]}),"\n",(0,c.jsxs)(n.h2,{id:"nginx-setup-for-switchmap-ng",children:["Nginx setup for ",(0,c.jsx)(n.code,{children:"switchmap-ng"})]}),"\n",(0,c.jsxs)(n.p,{children:[(0,c.jsx)(n.code,{children:"switchmap-ng"})," has sample configurations for the Nginx webserver."]}),"\n",(0,c.jsxs)(n.p,{children:["Run the following commands from the top directory of ",(0,c.jsx)(n.code,{children:"switchmap-ng"})]}),"\n",(0,c.jsx)(n.pre,{children:(0,c.jsx)(n.code,{className:"language-bash",children:"$ sudo cp examples/linux/nginx/switchmap-ng-nginx.conf /etc/nginx/sites-available\n$ sudo ln -s /etc/nginx/sites-available/switchmap-ng-nginx.conf /etc/nginx/conf-enabled/switchmap-ng-nginx.conf \n"})}),"\n",(0,c.jsxs)(n.p,{children:[(0,c.jsx)(n.strong,{children:"Note:"})," Edit the ",(0,c.jsx)(n.code,{children:"/etc/nginx/conf-enabled/switchmap-ng-nginx.conf"}),"\nfile and change the IP address of the server then restart Nginx."]}),"\n",(0,c.jsx)(n.pre,{children:(0,c.jsx)(n.code,{className:"language-bash",children:"$ systemctl restart nginx.service\n"})}),"\n",(0,c.jsxs)(n.p,{children:["You should now be able to access your ",(0,c.jsx)(n.code,{children:"switchmap-ng"})," web pages using the\nfollowing link."]}),"\n",(0,c.jsxs)(n.ul,{children:["\n",(0,c.jsx)(n.li,{children:"http://SERVER_NAME/switchmap-ng/"}),"\n"]})]})}function d(e={}){const{wrapper:n}={...(0,i.R)(),...e.components};return n?(0,c.jsx)(n,{...e,children:(0,c.jsx)(h,{...e})}):h(e)}},8453:(e,n,s)=>{s.d(n,{R:()=>r,x:()=>o});var t=s(6540);const c={},i=t.createContext(c);function r(e){const n=t.useContext(i);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function o(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(c):e.components||c:r(e.components),t.createElement(i.Provider,{value:n},e.children)}}}]);
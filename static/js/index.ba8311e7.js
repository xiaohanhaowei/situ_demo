(function(e){function n(n){for(var a,c,u=n[0],d=n[1],f=n[2],l=0,i=[];l<u.length;l++)c=u[l],Object.prototype.hasOwnProperty.call(o,c)&&o[c]&&i.push(o[c][0]),o[c]=0;for(a in d)Object.prototype.hasOwnProperty.call(d,a)&&(e[a]=d[a]);m&&m(n);while(i.length)i.shift()();return r.push.apply(r,f||[]),t()}function t(){for(var e,n=0;n<r.length;n++){for(var t=r[n],a=!0,c=1;c<t.length;c++){var u=t[c];0!==o[u]&&(a=!1)}a&&(r.splice(n--,1),e=d(d.s=t[0]))}return e}var a={},c={index:0},o={index:0},r=[];function u(e){return d.p+"js/"+({}[e]||e)+"."+{"chunk-2d0af619":"5368ec64","chunk-2d221c57":"797b9dda","chunk-4febd4a1":"fe47d566","chunk-ce115b5a":"b81f7651","chunk-43247501":"28cddfe5","chunk-57c4bdfc":"d24313bb","chunk-2f359ac4":"944a193f","chunk-b6a4b148":"744e3e07","chunk-d57c6b10":"fc36328d"}[e]+".js"}function d(n){if(a[n])return a[n].exports;var t=a[n]={i:n,l:!1,exports:{}};return e[n].call(t.exports,t,t.exports,d),t.l=!0,t.exports}d.e=function(e){var n=[],t={"chunk-4febd4a1":1,"chunk-43247501":1,"chunk-2f359ac4":1,"chunk-b6a4b148":1,"chunk-d57c6b10":1};c[e]?n.push(c[e]):0!==c[e]&&t[e]&&n.push(c[e]=new Promise((function(n,t){for(var a="css/"+({}[e]||e)+"."+{"chunk-2d0af619":"31d6cfe0","chunk-2d221c57":"31d6cfe0","chunk-4febd4a1":"71d8079a","chunk-ce115b5a":"31d6cfe0","chunk-43247501":"100e07d3","chunk-57c4bdfc":"31d6cfe0","chunk-2f359ac4":"3b6ac4dd","chunk-b6a4b148":"94e4e563","chunk-d57c6b10":"11f7fd78"}[e]+".css",o=d.p+a,r=document.getElementsByTagName("link"),u=0;u<r.length;u++){var f=r[u],l=f.getAttribute("data-href")||f.getAttribute("href");if("stylesheet"===f.rel&&(l===a||l===o))return n()}var i=document.getElementsByTagName("style");for(u=0;u<i.length;u++){f=i[u],l=f.getAttribute("data-href");if(l===a||l===o)return n()}var m=document.createElement("link");m.rel="stylesheet",m.type="text/css",m.onload=n,m.onerror=function(n){var a=n&&n.target&&n.target.src||o,r=new Error("Loading CSS chunk "+e+" failed.\n("+a+")");r.code="CSS_CHUNK_LOAD_FAILED",r.request=a,delete c[e],m.parentNode.removeChild(m),t(r)},m.href=o;var p=document.getElementsByTagName("head")[0];p.appendChild(m)})).then((function(){c[e]=0})));var a=o[e];if(0!==a)if(a)n.push(a[2]);else{var r=new Promise((function(n,t){a=o[e]=[n,t]}));n.push(a[2]=r);var f,l=document.createElement("script");l.charset="utf-8",l.timeout=120,d.nc&&l.setAttribute("nonce",d.nc),l.src=u(e);var i=new Error;f=function(n){l.onerror=l.onload=null,clearTimeout(m);var t=o[e];if(0!==t){if(t){var a=n&&("load"===n.type?"missing":n.type),c=n&&n.target&&n.target.src;i.message="Loading chunk "+e+" failed.\n("+a+": "+c+")",i.name="ChunkLoadError",i.type=a,i.request=c,t[1](i)}o[e]=void 0}};var m=setTimeout((function(){f({type:"timeout",target:l})}),12e4);l.onerror=l.onload=f,document.head.appendChild(l)}return Promise.all(n)},d.m=e,d.c=a,d.d=function(e,n,t){d.o(e,n)||Object.defineProperty(e,n,{enumerable:!0,get:t})},d.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},d.t=function(e,n){if(1&n&&(e=d(e)),8&n)return e;if(4&n&&"object"===typeof e&&e&&e.__esModule)return e;var t=Object.create(null);if(d.r(t),Object.defineProperty(t,"default",{enumerable:!0,value:e}),2&n&&"string"!=typeof e)for(var a in e)d.d(t,a,function(n){return e[n]}.bind(null,a));return t},d.n=function(e){var n=e&&e.__esModule?function(){return e["default"]}:function(){return e};return d.d(n,"a",n),n},d.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},d.p="",d.oe=function(e){throw console.error(e),e};var f=window["webpackJsonp"]=window["webpackJsonp"]||[],l=f.push.bind(f);f.push=n,f=f.slice();for(var i=0;i<f.length;i++)n(f[i]);var m=l;r.push([0,"chunk-vendors"]),t()})({0:function(e,n,t){e.exports=t("56d7")},2395:function(e,n,t){},"56d7":function(e,n,t){"use strict";t.r(n);t("e260"),t("e6cf"),t("cca6"),t("a79d");var a=t("2b0e"),c=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},o=[],r=(t("7c55"),t("2877")),u={},d=Object(r["a"])(u,c,o,!1,null,null,null),f=d.exports,l=(t("d3b7"),t("8c4f")),i={path:"/labelManagement",meta:{title:"标签管理",icon:"coin"},component:function(){return t.e("chunk-2d0af619").then(t.bind(null,"0da0"))},children:[{meta:{special:!0},path:"",component:function(){return Promise.all([t.e("chunk-ce115b5a"),t.e("chunk-43247501")]).then(t.bind(null,"096c"))}}]},m=i,p={path:"/learningPlatform",meta:{title:"学习平台",icon:"tickets"},component:function(){return t.e("chunk-2d0af619").then(t.bind(null,"0da0"))},children:[{meta:{keepAlive:!0},path:"",component:function(){return Promise.all([t.e("chunk-ce115b5a"),t.e("chunk-57c4bdfc"),t.e("chunk-2f359ac4")]).then(t.bind(null,"7dbb"))}},{meta:{},props:function(e){return e.query},path:"semanticAnnotation",component:function(){return Promise.all([t.e("chunk-ce115b5a"),t.e("chunk-57c4bdfc"),t.e("chunk-b6a4b148")]).then(t.bind(null,"85a6"))}}]},h=p,s={path:"/login",component:function(){return t.e("chunk-4febd4a1").then(t.bind(null,"bd01"))}},b=s,k={path:"/404",component:function(){return t.e("chunk-2d221c57").then(t.bind(null,"cc89"))}},v=k,g=l["a"].prototype.push;l["a"].prototype.push=function(e){return g.call(this,e).catch((function(e){return e}))},a["default"].use(l["a"]);var y=[{path:"/",component:function(){return Promise.all([t.e("chunk-ce115b5a"),t.e("chunk-d57c6b10")]).then(t.bind(null,"c1f7"))},redirect:"/learningPlatform",children:[h,m]},b,v,{path:"*",redirect:"/404"}],w=new l["a"]({base:"",routes:y}),P=w,j=t("2f62");a["default"].use(j["a"]);var O=new j["a"].Store({state:{},mutations:{},actions:{},modules:{}}),x=(t("b0c0"),t("9e1f"),t("450d"),t("6ed5")),_=t.n(x),E=(t("0fb7"),t("f529")),S=t.n(E),A=(t("be4f"),t("896a")),T=t.n(A),C=(t("06f1"),t("6ac9")),$=t.n(C),L=(t("b84d"),t("c216")),M=t.n(L),N=(t("8f24"),t("76b9")),q=t.n(N),B=(t("28b2"),t("c7ad")),D=t.n(B),J=(t("6b30"),t("c284")),F=t.n(J),H=(t("bd49"),t("18ff")),I=t.n(H),K=(t("960d"),t("defb")),U=t.n(K),z=(t("cb70"),t("b370")),G=t.n(z),Q=(t("920a"),t("4f0c")),R=t.n(Q),V=(t("560b"),t("dcdc")),W=t.n(V),X=(t("826b"),t("c263")),Y=t.n(X),Z=(t("e612"),t("dd87")),ee=t.n(Z),ne=(t("075a"),t("72aa")),te=t.n(ne),ae=(t("9c49"),t("6640")),ce=t.n(ae),oe=(t("d2ac"),t("95b0")),re=t.n(oe),ue=(t("672e"),t("101e")),de=t.n(ue),fe=(t("5466"),t("ecdf")),le=t.n(fe),ie=(t("38a0"),t("ad41")),me=t.n(ie),pe=(t("8bd8"),t("4cb2")),he=t.n(pe),se=(t("4ca3"),t("443e")),be=t.n(se),ke=(t("a769"),t("5cc3")),ve=t.n(ke),ge=(t("a7cc"),t("df33")),ye=t.n(ge),we=(t("0c67"),t("299c")),Pe=t.n(we),je=(t("f225"),t("89a9")),Oe=t.n(je),xe=(t("5e32"),t("6721")),_e=t.n(xe),Ee=(t("b8e0"),t("a4c4")),Se=t.n(Ee),Ae=(t("f4f9"),t("c2cc")),Te=t.n(Ae),Ce=(t("7a0f"),t("0f6c")),$e=t.n(Ce),Le=(t("10cb"),t("f3ad")),Me=t.n(Le),Ne=(t("eca7"),t("3787")),qe=t.n(Ne),Be=(t("425f"),t("4105")),De=t.n(Be),Je=(t("de31"),t("c69e")),Fe=t.n(Je),He=(t("a673"),t("7b31")),Ie=t.n(He),Ke=(t("adec"),t("3d2d")),Ue=t.n(Ke),ze=(t("6611"),t("e772")),Ge=t.n(ze),Qe=(t("1f1a"),t("4e4b")),Re=t.n(Qe),Ve=(t("1951"),t("eedf")),We=t.n(Ve);a["default"].component(We.a.name,We.a),a["default"].component(Re.a.name,Re.a),a["default"].component(Ge.a.name,Ge.a),a["default"].component(Ue.a.name,Ue.a),a["default"].component(Ie.a.name,Ie.a),a["default"].component(Fe.a.name,Fe.a),a["default"].component(De.a.name,De.a),a["default"].component(qe.a.name,qe.a),a["default"].component(Me.a.name,Me.a),a["default"].component($e.a.name,$e.a),a["default"].component(Te.a.name,Te.a),a["default"].component(Se.a.name,Se.a),a["default"].component(_e.a.name,_e.a),a["default"].component(Oe.a.name,Oe.a),a["default"].component(Pe.a.name,Pe.a),a["default"].component(ye.a.name,ye.a),a["default"].component(ve.a.name,ve.a),a["default"].component(be.a.name,be.a),a["default"].component(he.a.name,he.a),a["default"].component(me.a.name,me.a),a["default"].component(le.a.name,le.a),a["default"].component(de.a.name,de.a),a["default"].component(re.a.name,re.a),a["default"].component(ce.a.name,ce.a),a["default"].component(te.a.name,te.a),a["default"].component(ee.a.name,ee.a),a["default"].component(Y.a.name,Y.a),a["default"].component(W.a.name,W.a),a["default"].component(R.a.name,R.a),a["default"].component(G.a.name,G.a),a["default"].component(U.a.name,U.a),a["default"].component(I.a.name,I.a),a["default"].component(F.a.name,F.a),a["default"].component(D.a.name,D.a),a["default"].component(q.a.name,q.a),a["default"].component(M.a.name,M.a),a["default"].component($.a.name,$.a),a["default"].use(T.a.directive),a["default"].prototype.$loading=T.a.service,a["default"].prototype.$message=S.a,a["default"].prototype.$confirm=_.a.confirm;t("6a1d");var Xe=t("5a0c"),Ye=t("0ecf"),Ze=t("f906");Xe.extend(Ye),Xe.extend(Ze),a["default"].config.productionTip=!1,a["default"].prototype.$dayjs=Xe,a["default"].prototype.$bus=new a["default"],new a["default"]({router:P,store:O,render:function(e){return e(f)}}).$mount("#app")},"6a1d":function(e,n,t){},"7c55":function(e,n,t){"use strict";var a=t("2395"),c=t.n(a);c.a}});
//# sourceMappingURL=index.ba8311e7.js.map
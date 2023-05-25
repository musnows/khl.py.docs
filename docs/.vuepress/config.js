module.exports = {
  // 网站的一些基本配置
  // base:配置部署站点的基础路径，后续再介绍
  title: 'khl.py', // 网站的标题
  description: 'khl.py 文档', // 网站的描述，它将会以 <meta> 标签渲染到当前页面的 HTML 中。
  head: [
    ['link', { rel: 'icon', href: '/img/logo.png' }],
    ['script', {charset:'UTF-8',id:'LA_COLLECT',src:'//sdk.51.la/js-sdk-pro.min.js'}],
    ['script', {}, `LA.init({id:"K4jpll24hC6vwBJ0",ck:"K4jpll24hC6vwBJ0"})`]
  ],// 需要被注入到当前页面的 HTML <head> 中的标签
  base:'/',
  themeConfig: {
    logo: '/img/logo.png',
    nav: [
      { text: '主页', link: '/' },
      { text: '文档', link: '/docs/' },
      { text: 'Github', link: 'https://github.com/TWT233/khl.py' },
      { text: 'KOOK', link: 'https://kook.top/exKy0f' },
    ]
  }
}
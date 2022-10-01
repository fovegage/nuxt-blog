const axios = require('axios');

const apiurl = 'http://148.70.157.111:8004';
export default {
  mode: 'universal',
  head: {
    title: '自由之书 | 现代版外网百科全书',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0'},
      {name: 'format-detection', content: 'telephone=no'}
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
    ],
    script: [
      {src: '//at.alicdn.com/t/font_994113_26x7ecyei4d.js'},
      {src: '/js/prism.js'},
      // 百度主推文章收录用
      {src: 'https://zz.bdstatic.com/linksubmit/push.js'},
      // baidu analysis
      {src: 'https://hm.baidu.com/hm.js?75fd7a062cf64d7693f4f8422db3ffbf'}
      // google analysis
    ]
  },

  loading: './components/Loading',

  router: {
    middleware: 'global'
  },

  css: [
    'element-ui/lib/theme-chalk/index.css',
    './assets/scss/global.scss'
  ],

  styleResources: {
    scss: ['./assets/scss/variable.scss']
  },

  plugins: [
    '~/plugins/axios',
    {src: '~/plugins/element-ui', ssr: true},
    {src: '~/plugins/message', ssr: false},
    {src: '~/plugins/icon', ssr: true}
    // { src: '~/plugins/common', ssr: false }
  ],

  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/style-resources',
    '@nuxtjs/proxy',
    '@nuxtjs/sitemap'
  ],

  axios: {
    proxy: true,
    credentials: true
  },
  build: {
    transpile: [/^element-ui/],
    extractCSS: true,
    vendors: ['@nuxtjs/axios', 'element-ui']
    // extend (config, { isDev, isClient }) {
    //   if (isClient && !isDev) {
    //     config.output.futureEmitAssets = false
    //     config.plugins.push(qiniuPlugin);// 添加插件
    //     config.output.publicPath = '//cdn.com/fe/dist/' // 自己配置
    //   }
    // },
    // 可以使用腾讯cos，研究文件如何上传
    // publicPath: 'https://img-1301479650.cos.ap-shanghai.myqcloud.com/'
  },
  // axios: {
  //   // See https://github.com/nuxt-community/axios-module#options
  //   proxy: true, // 表示开启代理
  //   // prefix: '/api', // 表示给请求url加个前缀 /api
  //   credentials: true // 表示跨域请求时是否需要使用凭证
  // },
  // nuxt.js service 在这里没有用 研究xuammo的servie 看是否可以和django结合
  proxy: {
    '/api': {
      // target: 'https://www.xuanmo.xin',
      target: apiurl,
      pathRewrite: {
        '^/api': ''
      }
    }
    // '/api/*': {
    //   target: 'http://127.0.0.1:8866',
    //   pathRewrite: {
    //     '^/api': '/api'
    //   }
    // }
  },

  env: {
    // baseUrl: '/api'
    // baseUrl: 'http://127.0.0.1:8866'
    baseUrl: apiurl
  },
  site: {
    domain: 'https://www.vpnbook.cn',
    type: 2
  },
  // sitemap: {
    // path: '/sitemap.xml', // sitemap文件名，不用改
    // hostname: 'https://www.gaozhe.net', // 网址
    // cacheTime: 60 * 60 * 6, // 更新频率，只在 generate: false有用
    // gzip: true, // 生成 .xml.gz 压缩的 sitemap
    // generate: false, // 允许使用 nuxt generate 生成
    // 排除不要页面
    // exclude: [
    //   '/404',
    //   '/page',
    //   '/details',
    //   '/article',
    //   '/tags',
    //   '/category',
    //   '/search'
    // ],
    // 页面路由
    // routes(callback) {
    //   axios.all([
    //     // blog 分类
    //     axios.get(apiurl, {
    //       params: {
    //         type: 2
    //       }
    //     }),
    //     // 文章列表
    //     axios.get(apiurl, {
    //       params: {
    //         type: 2,
    //         page: 1,
    //         per_page: 100,
    //         _embed: true
    //       },
    //       data: {progress: false}
    //     }),
    //     // 标签
    //     axios.get(apiurl, {
    //       params: {
    //         type: 2
    //       }
    //     })
    //
    //   ]).then(axios.spread(function (menu, posts, info) {
    //     let now = new Date();
    //     now.setHours(now.getHours(), now.getMinutes() - now.getTimezoneOffset());
    //     let indexRoutes = [
    //       {
    //         url: '/',
    //         changefreq: 'daily',
    //         priority: 1,
    //         lastmodISO: now.toISOString()
    //       }
    //     ]
    //     let menuRoutes = menu.data.map((data) => {
    //       let url = ''
    //       if (data.ctype === 1) {
    //         url = '/category/1?type=' + data.id + '&title=' + data.cname
    //       }
    //       if (data.ctype === 2) {
    //         url = '/page/' + data.id
    //       }
    //       return {
    //         url: url,
    //         changefreq: 'monthly',
    //         priority: 0.8,
    //         lastmodISO: data.add_time
    //       }
    //     });
    //     let postsRoutes = posts.data.results.map((data) => {
    //       return {
    //         url: '/details/' + data.id,
    //         changefreq: 'daily',
    //         priority: 0.9,
    //         lastmodISO: data.update_at
    //       }
    //     });
    //     let tagsRoutes = info.data[0].blog_tag.map((data) => {
    //       return {
    //         url: `/tags/1?type=${data.id}&title=${data.tname}`,
    //         changefreq: 'weekly',
    //         priority: 0.7,
    //         lastmodISO: data.add_time
    //       }
    //     })
    //     // 用 concat 進行合併
    //     callback(null, indexRoutes.concat(menuRoutes, postsRoutes, tagsRoutes));
    //   }), function (err) {
    //     throw (err);
    //   });
    // }
  // }
}

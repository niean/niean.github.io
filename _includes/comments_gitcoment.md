<!-- 评论组件 -->
<div id="comments_container"></div>
<link rel="stylesheet" href="https://imsun.github.io/gitment/style/default.css">
<script src="https://imsun.github.io/gitment/dist/gitment.browser.js"></script>

<script>
var gitment = new Gitment({
  id: '',
  owner: 'niean',
  repo: 'niean.common.store.git',
  oauth: {
    client_id: '9fc62ffa7026d4a3f1a8',
    client_secret: 'bb4f02ffcf63cbc4c8248234f198dbdad65af61f',
  },
})
gitment.render('comments_container')
</script>
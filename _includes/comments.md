<!-- 评论组件 -->
<div id="vcomments"></div>
<script src="//cdn1.lncld.net/static/js/3.0.4/av-min.js"></script>
<script src='//unpkg.com/valine/dist/Valine.min.js'></script>
<script>
    new Valine({
        el: '#vcomments' ,
        appId: 'xiXnUFTTVsjwOj3RMdrgLY5w-gzGzoHsz',
        appKey: 'jYgD3fF22rW5RS15dBywkiOs',
        notify: false, 
        verify: false, 
        avatar: 'mm', 
        visitor: true,
        placeholder: '评论区'
    });
</script>
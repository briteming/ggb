# github-blog

自从学习Python以来，一直有个自己写一个博客页面的想法，今天终于初步实现了。

**原理非常简单**：

1. 使用 PyGithub 读取 GitHub 仓库的 issues
   > 可以返回 issue 的标题、创建时间、标签、内容等
2. 利用 GitHub API 将第一步得到的 markdown 格式的 issue 内容转换为 HTML
3. 使用 Jinja2 写一个HTML模板，并将第一步得到的内容渲染

**demo**

[geoqiao's pages](https://geoqiao.github.io/contents)
目前还很简陋，但能写到这样已经很开心了

## 使用方法

```bash
# 安装Python、并安装依赖后
python main.py <github_token> <github_repo>
```

## ROADMAP && TODO

- [x] 优化HTML模板（尽力了...等更熟悉 CSS 之后再搞
- [x] 增加 GitHub Actions 支持，实现 issue 更新后自动部署
- [ ] 慢慢优化代码（现在优先实现功能、优化先放一放
- [x] 分享搭建的过程，输出中巩固
- [ ] 增加基于 issue 的评论功能

## 非常感谢：

**[gitblog](https://github.com/yihong0618/gitblog)**

我之前使用的是 yihong 老师的 gitblog ~~(自己写的还没能完全自动化)~~，也是从 yihong 老师这里第一次看到了用issue写博客，还能用 GitHub 和 Python 实现几乎完全自动化，真是太牛了。如果有写博客的需求，强烈推荐这个项目。

**[Gmeek](https://github.com/Meekdai/Gmeek)**

关注Gmeek项目也很久，从这里知道了如何使用 GitHub API 实现 markdown 转 HTML。这个项目已经很完善，按教程操作走，很快就可以实现 GitHub Pages 的搭建。

以及 **Gemini/poe** 等一大批 ai 工具，作为编程初学者赶上这个两年，真的受益良多

<template>
  <div>
    <!-- 公告栏 -->
    <div v-if="sidebar.notice" class="sidebar-list notice">
      <div class="header">
        <p>
          <x-icon type="icon-notice1"></x-icon> 公告
        </p>
      </div>
      <div class="content" v-html="sidebar.notice"></div>
    </div>

    <div v-if="sidebar.notice" class="sidebar-list notice">
      <div class="header">
        <p>
          <x-icon type="icon-wechat"></x-icon> 公众号
        </p>
      </div>
      <img class="content" :src="sidebar.wechat">
    </div>
    <!-- 最新评论 -->
<!--    <div class="sidebar-list comment">-->
<!--      <div class="header">-->
<!--        <p>-->
<!--          <x-icon type="icon-hot1"></x-icon> 最新评论-->
<!--        </p>-->
<!--      </div>-->
<!--      <ul class="content">-->
<!--        <li class="list" v-for="item in sidebar.newComment" :key="item.key">-->
<!--          <template>-->
<!--            <p v-if="sidebar.isOpenTextThumbnail" class="thumbnail-text" :style="{ background: item.background }">-->
<!--              {{ item.author.substr(0, 1) }}-->
<!--            </p>-->
<!--            <img v-else :src="item.avatar" class="thumbnail" width="50" height="50">-->
<!--          </template>-->
<!--          <div class="right">-->
<!--            <h3 class="author">{{ item.author }}</h3>-->
<!--            <p class="comment-text" v-html="item.content.replace(/\[img\]\S+\[\/img\]/, '[图片]')"></p>-->
<!--            <nuxt-link v-if="item.postType === 'post'" :to="{ name: 'details-id', params: { id: item.id } }" class="block title">评：{{ item.title }}</nuxt-link>-->
<!--            <nuxt-link v-else-if="item.postType === 'page'" :to="{ name: 'page-id', params: { id: item.id } }" class="block title">评：{{ item.title }}</nuxt-link>-->
<!--          </div>-->
<!--        </li>-->
<!--      </ul>-->
<!--    </div>-->
    <!-- 站点统计 -->
    <div class="sidebar-list count">
      <div class="header">
        <p>
          <x-icon type="icon-count"></x-icon> 站点统计
        </p>
      </div>
      <ul class="content">
        <li class="list">标签：{{ sidebar.getAllCountTag }}个</li>
        <li class="list">文章：{{ sidebar.getAllCountArticle }}篇</li>
        <li class="list">页面：{{Math.ceil(sidebar.getAllCountArticle / 8)}}个</li>
        <li class="list">评论：{{ sidebar.getAllCountComment }}条</li>
        <li class="list">分类：{{ sidebar.getAllCountCat }}个</li>
        <li class="list">最后更新：{{ sidebar.lastUpDate }}</li>
      </ul>
    </div>
    <!-- 标签云 -->
    <div class="sidebar-list tag-cloud">
      <div class="header">
        <p>
          <x-icon type="icon-tag1"></x-icon> 标签云
        </p>
        <router-link :to="{ name: 'tags' }">更多</router-link>
      </div>
      <ul class="content">
        <template v-for="(item, index) in sidebar.tagCloud">
          <li :key="item.key" v-if="index < 20" class="list" :class="`color-${Math.floor(Math.random() * 8) + 1}`">
            <router-link :to="{ name: 'tags-id', params: { id: 1 }, query: { type: item.id, title: item.tname } }">{{ item.tname }}</router-link>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'AppSidebar',
  computed: {
    ...mapState({
      sidebar: state => ({
        notice: state.info.notice,
        wechat: state.info.wechat,
        newComment: state.info.newComment,
        isOpenTextThumbnail: state.info.isOpenTextThumbnail,
        // isOpenAsideCount: state.info.isOpenAsideCount,
        getAllCountTag: state.base.tcount,
        getAllCountArticle: state.base.pcount,
        // getAllCountPage: state.base.page,
        getAllCountComment: state.base.comments,
        getAllCountCat: state.base.ccount,
        lastUpDate: state.base.last_essay,
        tagCloud: state.tags
      })
    })
  }
}
</script>

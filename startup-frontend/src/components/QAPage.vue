<template>
    <div>
      <h2>Q&A Section</h2>
      <QAPostList />
      <AskQAPost />
    </div>
  </template>
  
  <script>
  import QAPostList from './QAPostList.vue';
  import AskQAPost from './AskQAPost.vue';
  
  export default {
    components: {
      QAPostList,
      AskQAPost,
    },
  };
  </script>
  
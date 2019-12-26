<template>
    <div class="player">
      <div id="player"></div>
    </div>
</template>

<script>
export default {
  name:"Player",
  data () {
    return {

    }
  },
  mounted(){
      let user_token = this.$settings.check_user_login();
      let user_name = localStorage.user_name || sessionStorage.user_name;
      let self = this;
      if(!user_token){
          this.$alert("您尚未登录，请登录后再进行操作！","路飞学城",{
              callback(){
                self.$router.push("/login");
              }
          });
          return;
      }

      // 去后台读取课程对应的视频vid，自己补充
      let vid = "0411ff75f685f81f5ed1a7af11810895_0";
      var player = polyvObject('#player').videoPlayer({
        wrap: '#player',
        width: document.documentElement.clientWidth-260, // 页面宽度
        height: document.documentElement.clientHeight,   // 页面高度
        forceH5: true,
        vid: vid,
        code: user_name, // 一般是用户昵称
        // 视频加密播放的配置
        playsafe: function (vid, next) { // 向后端发送请求获取加密的token
            self.$axios.get(`${self.$settings.Host}/courses/player/`,{
              params:{
                vid: vid,
              },
              headers:{
                "Authorization":"jwt " + user_token,
              }
            }).then(function (response) {
                console.log(response);
                next(response.data);
            })
        }
    });
  },
  methods: {

  },
  computed: {
  }
}
</script>

<style scoped>
</style>

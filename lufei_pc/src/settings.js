export default {
  // 服务端的api地址
  Host: "http://api.yangsenjacob.club",
  check_user_login(){
    return localStorage.user_token || sessionStorage.user_token;
  }
}

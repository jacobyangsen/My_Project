<template>
	<div class="box">
		<img src="/static/image/Loginbg.3377d0c.jpg" alt="">
		<div class="register">
      <div class="login-title">
				<img src="/static/image/Logotitle.1ba5466.png" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
			<div class="register_box">
        <div class="register-title">注册路飞学城</div>
				<div class="inp">
					<input v-model = "mobile" type="text" @blur="check_mobile" placeholder="手机号码" class="user">
					<input v-model = "password" type="password" placeholder="输入密码" class="user">
		      <div class="sms-box">
            <input v-model = "sms" type="text" placeholder="输入验证码" class="user">
            <div class="sms-btn" @click="smsHandle">{{interval_text}}</div>
          </div>
          <div id="geetest"></div>
          <button class="register_btn" @click="registerHandle">注册</button>
					<p class="go_login" >已有账号 <router-link to="/login">直接登录</router-link></p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'Register',
  data(){
    return {
        sms:"",
        mobile:"",
        password:"",
        interval_text: "点击发送短信",
        is_send_interval:false, // 是否在60秒内发送短信的状态，false表示没有
    }
  },
  created(){

  },
  methods:{
      check_mobile(){
          // 验证格式
          if( ! /^1[3-9]\d{9}$/.test(this.mobile) ){
              this.$message.error("对不起，手机号格式不正确！");
              return ;
          }

          // 验证是否被注册了
          this.$axios.get(`${this.$settings.Host}/user/mobile/${this.mobile}/`).then(response=>{

          }).catch(error=>{
              if(error.response.status === 400){
                  this.$message.error("对不起，当前手机已被注册！");
              }else{
                  this.$message.error("网络异常，请联系网站客服工作人员！");
              }
          });
      },
      smsHandle(){
          // 判断是否在60内曾经有发送短信的记录
          if(this.is_send_interval){
              this.$message.error("请不要频繁点击发送短信！");
              return ;
          }
          // 短信发送处理
          this.$axios.get(`${this.$settings.Host}/user/sms/${this.mobile}/`).then(response=>{
              if(response.data.status){
                  this.$message.success("短信已发送，请注意留意您的手机！");
                  // 更新发送短信的间隔状态
                  this.is_send_interval = true;
                  let time = 60;
                  let t = setInterval(()=>{
                      if(time<1){
                          this.interval_text = "点击发送短信";
                          this.is_send_interval = false; // 允许用户重新点击发送短信
                          clearInterval(t); // 关闭定时器
                      }else{
                          time--;
                          this.interval_text = `${time}后点击重新发送`
                      }
                  },1000);
              }
          }).catch(error=>{
              this.$message.error("对不起，发送短信失败！");
          })
      },
      registerHandle(){
          // 注册处理
          this.$axios.post(`${this.$settings.Host}/user/`, {
              mobile:this.mobile,
              sms_code: this.sms,
              password: this.password,
          }).then(response=>{
              if(response.status===201){
                  // 注册成功
                  sessionStorage.user_token = response.data.token;
                  sessionStorage.user_id = response.data.id;
                  sessionStorage.user_name = response.data.username;
                  sessionStorage.user_credit = response.data.user_credit;
                  sessionStorage.credit_rmb = response.data.credit_rmb;

                  let self = this;
                  this.$alert("注册成功！","路飞学城",{
                      callback(){
                          self.$router.push("/");
                      }
                  })

              }else{
                  // 注册失败
                  this.$message.error("对不起，注册用户失败！请重新注册或联系网站客服工作人员！");
              }
          }).catch(error=>{
              this.$message.error("对不起，注册用户失败！请重新注册或联系网站客服工作人员！");
          })
      }
  },

};
</script>

<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .register {
	position: absolute;
	width: 500px;
	height: 400px;
	top: 0;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}
.register .register-title{
    width: 100%;
    font-size: 24px;
    text-align: center;
    padding-top: 30px;
    padding-bottom: 30px;
    color: #4a4a4a;
    letter-spacing: .39px;
}
.register-title img{
    width: 190px;
    height: auto;
}
.register-title p{
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.register_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}
.register_box .title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
	 display: flex;
    	justify-content: space-around;
    	padding: 50px 60px 0 60px;
    	margin-bottom: 20px;
    	cursor: pointer;
}
.register_box .title span:nth-of-type(1){
	color: #4a4a4a;
    	border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp input{
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
/*left: 20px;*/

}
#geetest{
	margin-top: 20px;
}
.register_btn{
     width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
.login-title{
    margin-top: 32px;
    width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.sms-box{
  position: relative;
}
.sms-btn{
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}
</style>

<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
        <h3 class="cart-top">购物车结算 <span>共{{course_list.length}}门课程</span></h3>
        <div class="cart-title">
           <el-row>
             <el-col :span="2">&nbsp;</el-col>
             <el-col :span="10">课程</el-col>
             <el-col :span="8">有效期</el-col>
             <el-col :span="4">价格</el-col>
           </el-row>
        </div>
        <div class="cart-item">
          <el-row :key="key" v-for="course,key in course_list">
             <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
             <el-col :span="10" class="course-info">
               <img :src="$settings.Host+course.course_img" alt="">
               <span class="course-title">{{course.name}}<br>{{course.discount_name}}</span>
             </el-col>
             <el-col :span="8"><span>{{course.expire}}</span></el-col>
             <el-col :span="4" class="course-price">¥{{course.discount_price}}<br><span>原价 ¥{{course.price.toFixed(2)}}</span></el-col>
           </el-row>
        </div>
        <div class="discount">
          <div id="accordion">
            <div class="coupon-box">
              <div class="icon-box">
                <span class="select-coupon">使用优惠劵：</span>
                <a class="select-icon" @click="use_coupon=!use_coupon"><img class="sign" :class="use_coupon?'is_show_select':''" src="../../static/image/12.png" alt=""></a>
                <span class="coupon-num">有{{coupon_list.length}}张可用</span>
              </div>
              <p class="sum-price-wrap">商品总金额：<span class="sum-price">{{total_price.toFixed(2)}}元</span></p>
            </div>
            <div id="collapseOne" v-if="use_coupon">
              <ul class="coupon-list">
                <li class="coupon-item" :class="{active:coupon==item.id,disable:check_coupon(item.start_time, item.coupon.duration) || total_price < item.coupon.condition || total_real_price < item.coupon.condition }" @click="click_coupon(item)" v-for="item in coupon_list">
                  <p class="coupon-name">{{item.coupon.name}}</p>
                  <p class="coupon-condition">满{{item.coupon.condition}}元可以使用</p>
                  <p class="coupon-time start_time">开始时间：{{item.start_time.replace("T"," ")}}</p>
                  <p class="coupon-time end_time">过期时间：{{has_time(item.start_time,item.coupon.duration)}}</p>
                </li>
              </ul>
              <div class="no-coupon" v-if="false">
                <span class="no-coupon-tips">暂无可用优惠券</span>
              </div>
            </div>
          </div>
          <div class="credit-box">
            <label class="my_el_check_box"><el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox></label>
            <p class="discount-num1" v-if="!use_credit">使用我的贝里</p>
            <p class="discount-num2" v-if="use_credit"><span>总积分：{{my_credit-current_credit}}，可以抵扣 <el-input-number :min="0" :max="max_credit(my_credit,total_price)" size="mini" v-model="current_credit"></el-input-number> 积分， 已抵扣￥{{current_credit/credit_rmb}}元</span></p>
          </div>
          <p class="sun-coupon-num">优惠券抵扣：<span>{{sale_price.toFixed(2)}}元</span></p>
        </div>
        <div class="calc">
            <el-row class="pay-row">
              <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
              <el-col :span="8">
                <span class="alipay" @click="pay_type=1" v-if="pay_type!=1"><img src="../../static/image/alipay.png" alt="支付宝"></span>
                <span class="alipay" v-if="pay_type==1"><img src="../../static/image/alipay2.png" alt="支付宝"></span>
                <span class="alipay wechat" @click="pay_type=2" v-if="pay_type!=2"><img src="../../static/image/wechat.png" alt="微信支付"></span>
                <span class="alipay wechat" v-if="pay_type==2"><img src="../../static/image/wechat2.png" alt="微信支付"></span>
              </el-col>
              <el-col :span="8" class="count">实付款： <span>¥{{total_real_price.toFixed(2)}}</span></el-col>
              <el-col :span="4" class="cart-pay"><span @click="ordeHander">立即支付</span></el-col>
            </el-row>
        </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default {
    name:"Order",
    data(){
      return {
        user_token: "",      // 用户的jwt token
        course_list: [],     // 勾选商品列表
        total_price: 0,      // 课程总价
        total_real_price: 0, // 实付总价
        sale_price: 0,       // 优惠券抵扣价格
        use_coupon: false, // 是否使用优惠券
        use_credit: false, // 是否使用积分
        coupon_list: [],    // 用户的优惠券列表
        coupon: 0,   // 当前用户选择的优惠券ID
        coupon_price: 0, // 优惠券抵扣价格
        my_credit: sessionStorage.user_credit || localStorage.user_credit,      // 当前用户拥有的积分
        credit_rmb: sessionStorage.credit_rmb || localStorage.credit_rmb,     // 积分兑换比率
        current_credit: 0, // 本次订单使用的积分
        credit_price: 0,  // 积分折算价格
        pay_type: 1,  // 支付方式
      }
    },
    components:{
      Header,
      Footer,
    },
    created(){
      this.user_token = this.$settings.check_user_login();
      this.get_selected_course();
      this.get_user_coupon();
    },
    watch:{
        coupon(){
            this.calc_total_price();
        },
        use_coupon(){
            // 是否使用了优惠券
            if(!this.use_coupon){
                this.coupon = 0;
            }
        },
        current_credit(){
            // 每次使用的积分发生变化时，都要重新计算新的总价格
            this.calc_total_price();
        },
        use_credit(){
            this.current_credit = 0;
            this.calc_total_price();
        }
    },
    methods: {
       has_time(start_time, timer){
          let start_timestamp = (new Date(start_time) - 0)/1000;
          let timer_timestamp = timer * 24 * 3600;
          let endtime_timestamp = start_timestamp + timer_timestamp;
          let endtime = new Date(endtime_timestamp * 1000);
          let year = endtime.getFullYear();
          let month = endtime.getMonth()+1;
          month = month>=10?month:"0"+month;
          let date = endtime.getDate();
          date = date >=10?date:"0"+date;
          let hour = endtime.getHours();
          hour = hour >=10?hour:"0"+hour;
          let min = endtime.getMinutes();
          min = min >= 10?min:"0"+min;
          let sec = endtime.getSeconds();
          sec = sec >= 10?sec:"0"+sec;
          let time = `${year}-${month}-${date} ${hour}:${min}:${sec}`;
          return time;
        },
        get_user_coupon(){
          // 获取登录的用户
            let user_id = localStorage.user_id || sessionStorage.user_id;
          // 获取当前用户的优惠券
          this.$axios.get(`${this.$settings.Host}/coupon/`,{
              params:{
                  user_id, // 等同于 user_id:user_id,
              },
              headers:{
                  "Authorization": "jwt " + this.user_token,
              }
          }).then(response=>{
              this.coupon_list = response.data;
          }).catch(error=>{
             this.$message.error("获取优惠券列表失败！");
          });
        },
        get_selected_course(){
            // 获取勾选的商品信息
            this.$axios.get(`${this.$settings.Host}/cart/selected/`,{
                headers:{
                    "Authorization": "jwt " + this.user_token,
                }
            }).then(response=>{
                this.course_list = response.data;
                let total_price = 0;
                for(let course of this.course_list){
                    total_price = total_price + parseFloat(course.discount_price);
                }
                this.total_price = total_price;
                this.total_real_price = total_price  - this.current_credit/this.credit_rmb;
            }).catch(error=>{
                this.$message.error("无法获取商品信息！");
            });
        },
        ordeHander(){
          // 生成订单
          this.$axios.post(`${this.$settings.Host}/orders/`,{
            "pay_type": this.pay_type,
            "credit": this.current_credit,  // 积分
            "coupon": this.coupon   // 优惠券
          },{
            headers:{
                "Authorization": "jwt " + this.user_token,
            }
          }).then(response=>{
            let order_number = response.data.order_number;
            // 扣除本地缓存的积分

            // 去支付
            this.payhander(order_number)
          }).catch(error=>{
            this.$message.error("生成订单失败！");
          })
        },
        payhander(order_number){
          // 去支付
          this.$axios.get(`${this.$settings.Host}/payments/alipay/`,{
              params:{
                  order_number,
              },
            headers:{
                "Authorization": "jwt " + this.user_token,
            }
          }).then(response=>{
              // 页面跳转到支付页面
              console.log(response.data.url);
              // location.href = response.data.url;
          }).catch(error=>{
              this.$message.error("对不起，网络繁忙，请稍后在个人中心订单列表中完成支付！");
          });
        },
        check_coupon(start_time,duration){
          // 判断优惠券是否已经过期
          let now = new Date() - 0;
          let duration_end = new Date(start_time) - 0 + duration * 24 * 3600 * 1000; // 过期时间戳
          let duration_start = new Date(start_time); // 起用时间戳

          return duration_start > now || duration_end<=now;
        },
        click_coupon(user_coupon){
            let result = this.check_coupon(user_coupon.start_time, user_coupon.coupon.duration) || this.total_price < user_coupon.coupon.condition || this.total_real_price < user_coupon.coupon.condition;
            if(!result){
              this.coupon=user_coupon.id;
            }
        },
        max_credit(user_credit, total_price){
           // 判断本次订单中用户允许使用最大积分
            let real_price_to_credit = (total_price - this.sale_price)  * this.credit_rmb;  // 实付总价转换成积分
            if(user_credit < real_price_to_credit){ // 用户积分比商品总价小
               return user_credit;
           }else{
               return parseInt(real_price_to_credit);
           }
        },
        calc_total_price(){
             if(this.coupon > 0){
                // 点选优惠券
                for(let user_coupon of this.coupon_list){
                    if(user_coupon.id == this.coupon){
                        let sale = parseFloat(user_coupon.coupon.sale.substr(1));
                        if( user_coupon.coupon.sale[0]=="*" ){
                            // 折扣
                            this.total_real_price = this.total_price * sale;
                            this.sale_price = this.total_price * (1-sale);
                        }else{
                            // 假面
                            this.total_real_price = this.total_price - sale;
                            this.sale_price = sale;
                        }
                    }
                }

            }else{
                this.total_real_price = this.total_price;
                this.sale_price = 0;
            }
            this.total_real_price = this.total_real_price -this.current_credit/this.credit_rmb;
        }
    }
  }
</script>

<style scoped>
.cart{
  margin-top: 80px;
}
.cart-info{
  overflow: hidden;
  width: 1200px;
  margin: auto;
}
.cart-top{
  font-size: 18px;
  color: #666;
  margin: 25px 0;
  font-weight: normal;
}
.cart-top span{
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
}
.cart-title{
    background: #F7F7F7;
    height: 70px;
}
.calc{
  margin-top: 25px;
  margin-bottom: 40px;
}

.calc .count{
  text-align: right;
  margin-right: 10px;
  vertical-align: middle;
}
.calc .count span{
    font-size: 36px;
    color: #333;
}
.calc .cart-pay{
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
}
.cart-item{
  height: 120px;
  line-height: 120px;
  margin-bottom: 30px;
}
.course-info img {
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
  float: left;
}
.course-title{
  float: left;
  line-height: 32px;
  margin-top: 26px;
}
.course-price{
  line-height: 32px;
  margin-top: 32px;
}
.course-price span{
  text-decoration: line-through;
  color: #5e5e5e;
}
.alipay{
  display: inline-block;
  height: 48px;
  cursor: pointer;
}
.alipay img{
  height: 100%;
  width:auto;
}

.pay-text{
  display: block;
  text-align: right;
  height: 100%;
  line-height: 100%;
  vertical-align: middle;
  margin-top: 20px;
}
.discount{
  text-align: right;
  margin-top: 30px;
}
.coupon-box{
  text-align: left;
  padding-bottom: 22px;
  padding-left:30px;
  border-bottom: 1px solid #e8e8e8;
}
.coupon-box::after{
  content: "";
  display: block;
  clear: both;
}
.icon-box{
  float: left;
}
.icon-box .select-coupon{
  float: left;
  color: #666;
  font-size: 16px;
}
.icon-box::after{
  content:"";
  clear:both;
  display: block;
}
.select-icon{
  width: 20px;
  height: 20px;
  float: left;
}
.select-icon img{
  max-height:100%;
  max-width: 100%;
  margin-left: 10px;
  margin-top: 2px;
  transform: rotate(-90deg);
  transition: transform .5s;
}
.is_show_select{
  transform: rotate(0deg)!important;
}
.coupon-num{
    height: 22px;
    line-height: 22px;
    padding: 0 5px;
    text-align: center;
    font-size: 12px;
    float: left;
    color: #fff;
    letter-spacing: .27px;
    background: #fa6240;
    border-radius: 2px;
    margin-left: 20px;
}
.sum-price-wrap{
    float: right;
    font-size: 16px;
    color: #4a4a4a;
    margin-right: 45px;
}
.sum-price-wrap .sum-price{
  font-size: 18px;
  color: #fa6240;
}

.no-coupon{
  text-align: center;
  width: 100%;
  padding: 50px 0px;
  align-items: center;
  justify-content: center; /* 文本两端对其 */
  border-bottom: 1px solid rgb(232, 232, 232);
}
.no-coupon-tips{
  font-size: 16px;
  color: #9b9b9b;
}
.credit-box{
  height: 30px;
  margin-top: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-end
}
.my_el_check_box{
  position: relative;
}
.my_el_checkbox{
  margin-right: 10px;
  width: 16px;
  height: 16px;
}
.discount-num1{
  color: #9b9b9b;
  font-size: 16px;
  margin-right: 45px;
}
.discount-num2{
  margin-right: 45px;
  font-size: 16px;
  color: #4a4a4a;
}
.sun-coupon-num{
  margin-right: 45px;
  margin-bottom:43px;
  margin-top: 40px;
  font-size: 16px;
  color: #4a4a4a;
  display: inline-block;
}
.sun-coupon-num span{
  font-size: 18px;
  color: #fa6240;
}
.coupon-list{
  margin: 20px 0;
}
.coupon-list::after{
  display: block;
  content:"";
  clear: both;
}
.coupon-item{
  float: left;
  margin: 15px 8px;
  width: 180px;
  height: 100px;
  padding: 5px;
  background-color: #fa3030;
  cursor: pointer;
}
.coupon-list .active{
  background-color: #fa9000;
}
.coupon-list .disable{
  cursor: not-allowed;
  background-color: #fa6060;
}
.coupon-condition{
  font-size: 12px;
  text-align: center;
  color: #fff;
}
.coupon-name{
  color: #fff;
  font-size: 24px;
  text-align: center;
}
.coupon-time{
  text-align: left;
  color: #fff;
  font-size: 12px;
}
</style>

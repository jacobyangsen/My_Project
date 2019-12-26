<template>
    <div class="cart_item">
      <div class="cart_column column_1">
        <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
      </div>
      <div class="cart_column column_2">
        <img :src="$settings.Host+course.course_img" alt="">
        <span><router-link :to="`/courses/${course.course_id}`">{{course.course_name}}</router-link></span>
      </div>
      <div class="cart_column column_3">
        <el-select v-model="course.expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
          <el-option v-for="item in course.expire_list" :label="item.text" :value="item.time" :key="item.time"></el-option>
        </el-select>
      </div>
      <div class="cart_column column_4">¥{{course.price}}</div>
      <div class="cart_column column_4"><span @click="cart_delete">删除</span></div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    props:["course"],
    data(){
      return {
        checked: false,
      }
    },
    created(){
        this.user_token = this.$settings.check_user_login();
    },
    watch:{
        "course.selected": function(){
            // 切换商品的勾选状态
            this.change_selected_status();
        },
        "course.expire": function(){
          this.change_course_expire();
        },
    },
    methods:{
        change_course_expire(){
            // 从expire_list中选出对应的课程价格
            for(let item of this.course.expire_list){ // for ... of 是es6的语法，可以在循环中获取数组的成员，而不是原来的for ..in 里面的下表索引
                if( this.course.expire == item.time ){
                    this.course.price = item.price;
                }
            }
            // 把当前本次选中的有效期选项同步到redis中
            this.$axios.put(`${this.$settings.Host}/cart/`,{
                course_id: this.course.course_id,
                time: this.course.expire
            },{
                headers:{ // 访问需要登录认证权限的api接口必须附带token到请求头中
                  "Authorization": "jwt " + this.user_token,
                }
            }).then(response=>{
                // 在切换勾选状态时，通知父组件条件总价格
                this.$emit("change_course", this.course);
            }).catch(error=>{
                this.$message.error("切换有效期选项失败！无法请求服务端，请联系客服工作人员！");
            })
        },
        change_selected_status(){
            // 切换商品的勾选状态
            this.$axios.patch(`${this.$settings.Host}/cart/`,{
                "course_id": this.course.course_id,
	              "selected": this.course.selected,
            },{
                headers:{ // 访问需要登录认证权限的api接口必须附带token到请求头中
                  "Authorization": "jwt " + this.user_token,
                }
            }).then(response=>{
                // 在切换勾选状态时，通知父组件条件总价格
                this.$emit("change_course", this.course);
            }).catch(error=>{
               this.$message.error("勾选状态切换失败！请刷新页面后重新尝试！");
            });
        },
        cart_delete(){
           // 让用户确认是否删除商品
           this.$confirm(`您确定要删除当前商品<${this.course.course_name}>么？`, '路飞学城', {
                  confirmButtonText: '删除',
                  cancelButtonText: '取消',
                  type: 'warning'
                }).then(() => { // 点击删除
                  this.deleteHandler();
                }).catch(() => {

                });
        },
        deleteHandler(){
            // 购物车删除商品
            this.$axios.delete(`${this.$settings.Host}/cart/`,{
                params:{
                    course_id: this.course.course_id,
                },
                headers:{
                    "Authorization": "jwt " + this.user_token,
                }
            }).then(response=>{
                // 通知父组件删除当前课程内容
                this.$emit("delete_cart");
                this.$message.success("操作成功！");
            }).catch(error=>{
                this.$message.error("操作失败！");
            });
        }

    }
}
</script>

<style scoped>
.cart_item::after{
  content: "";
  display: block;
  clear: both;
}
.cart_column{
  float: left;
  height: 250px;
}
.cart_item .column_1{
  width: 88px;
  position: relative;
}
.my_el_checkbox{
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}
.cart_item .column_2 {
  padding: 67px 10px;
  width: 520px;
  height: 116px;
}
.cart_item .column_2 img{
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
}
.cart_item .column_3{
  width: 197px;
  position: relative;
  padding-left: 10px;
}
.my_el_select{
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}
.cart_item .column_4{
  padding: 67px 10px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}

</style>

<template>
  <div class="course">
    <Header></Header>
    <div class="main">
      <!-- 筛选条件 -->
      <div class="condition">
        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <li :class="filters.category==0?'this':''" @click="filters.category=0">全部</li>
          <li :class="filters.category==item.id?'this':''" v-for="item in category_list" @click="filters.category=item.id">{{item.name}}</li>
        </ul>

        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选: </li>
            <li class="default" :class="filters.ordering=='id'?'this asc': (filters.ordering=='-id'?'this desc':'')" @click="select_ordering('id')">默认</li>
            <li class="hot" :class="filters.ordering=='students'?'this asc': (filters.ordering=='-students'?'this desc':'')" @click="select_ordering('students')">人气</li>
            <li class="price" :class="filters.ordering=='price'?'this asc': (filters.ordering=='-price'?'this desc':'')" @click="select_ordering('price')">价格</li>
          </ul>
          <p class="condition-result">共{{course_total}}个课程</p>
        </div>

      </div>
      <!-- 课程列表 -->
      <div class="course-list">
        <div class="course-item" v-for="course in course_list">
          <div class="course-image">
            <img :src="course.course_img" alt="">
          </div>
          <div class="course-info">
            <h3><router-link :to="`/courses/${course.id}`">{{course.name}}</router-link> <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span></h3>
<!--            <h3><router-link :to="{ path:`/courses/${course.id}`,query:{'uid':1} }">{{course.name}}</router-link> <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span></h3>-->
            <p class="teather-info">{{course.teacher.role_name}} {{course.teacher.name}} {{course.teacher.signature}} {{course.teacher.title}} <span>共{{course.lessons}}课时/{{course.lessons==course.pub_lessons?'更新完成':'已更新'+course.pub_lessons+'课时'}}</span></p>
            <ul class="lesson-list">
              <li v-for="lesson,key in course.recomment_lessons"><span class="lesson-title">0{{key+1}} | 第{{lesson.id}}节：{{lesson.name}}</span> <span class="free" v-if="lesson.free_trail">免费</span></li>
            </ul>
            <div class="pay-box">
              <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>
              <span class="discount-price" v-if="course.discount_name">￥{{course.discount_price}}元</span>
              <span class="discount-price" v-else>￥{{course.price}}元</span>
              <span class="original-price" v-if="course.discount_name">原价：{{course.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>
          </div>
        </div>
      </div>
      <el-pagination v-if="course_total>1"
        background
        :page-size="filters.size"
        :page-sizes="[2, 5, 10, 20]"
        layout="sizes, prev, pager, next"
        @size-change="handleSizeChange"
        :current-page="filters.page"
        @current-change="handleCurrentChange"
        :total="course_total">
      </el-pagination>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default {
      name: "Course",
      data(){
        return{
          filters:{
            page: 1,
            size: 5,
            category: 0, // 当前点击的课程分类ID，0表示默认值，全部
            ordering: "id", // id默认，students人气, price价格，如果值的左边有-减号，则表示倒叙，否则是正序
          },
          category_list: [], // 课程分类列表
          course_total: 0,   // 当前课程的总数量
          course_list: [
              {
                  teacher: {},
              }
          ],
        }
      },
      created(){
        this.get_course_category();
        this.get_course();
      },
      watch:{
        // 每次分类ID进行了修改，都要重新获取一次课程列表信息
        "filters.category": function(){
            this.filters.page = 1;
            this.get_course();
        },
        "filters.ordering": function(){
            this.get_course();
        },
        "filters.page": function(){
            this.get_course();
        },
        "filters.size": function(){
            this.filters.page = 1;
            // this.get_course();
        },
      },
      methods:{
          get_course_category(){
              // 获取课程分类
              this.$axios.get(`${this.$settings.Host}/courses/category/`).then(response=>{
                  this.category_list = response.data;
              }).catch(error=>{
                  this.$message.error("无法获取课程分类信息！");
              })
          },
          get_course(){
              // 获取课程列表
              let filters = {
                  "ordering": this.filters.ordering,
              };

              // 判断课程分类ID不是0，则需要指定分类到后端查询对应分类的数据，拼接参数
              if(this.filters.category != 0){
                  filters.course_category = this.filters.category;
              }

              filters.page = this.filters.page;
              filters.size = this.filters.size;

              // 获取课程信息
              this.$axios.get(`${this.$settings.Host}/courses/`,{
                  params: filters
              }).then(response=>{
                  this.course_list = response.data.results; // 课程列表
                  this.course_total = response.data.count;  // 课程总数
              }).catch(error=>{
                  this.$message.error("无法获取课程信息！");
              })
          },
          select_ordering(ordering){
              // 判断切换不同的排序方式
              if(ordering=="id"){
                 // 点击了默认
                 if(this.filters.ordering=="id"){
                     this.filters.ordering="-id";
                 }else{
                     this.filters.ordering="id";
                 }
              }else if(ordering=="students"){
                  // 点击了人气
                 if(this.filters.ordering=="students"){
                     this.filters.ordering="-students";
                 }else{
                     this.filters.ordering="students";
                 }
              }else if(ordering=="price"){
                  // 点击了价格
                 if(this.filters.ordering=="price"){
                     this.filters.ordering="-price";
                 }else{
                     this.filters.ordering="price";
                 }
              }
          },
          handleCurrentChange(page){
              // 切换页码
              this.filters.page = page;
          },
          handleSizeChange(size){
              // 切换单页显示数据量
              this.filters.size = size;
          }
      },
      components:{
        Header,
        Footer,
      }
  }
</script>



<style scoped>
  .course{
    background: #f6f6f6;
  }
  .course .main{
    width: 1100px;
    margin: 35px auto 0;
  }
  .course .condition{
    margin-bottom: 35px;
    padding: 25px 30px 25px 20px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
  }
  .course .cate-list{
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
    padding-bottom: 18px;
    margin-bottom: 17px;
  }
  .course .cate-list::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .cate-list li{
    float: left;
    font-size: 16px;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
    border: 1px solid transparent; /* transparent 透明 */
  }
  .course .cate-list .title{
    color: #888;
    margin-left: 0;
    letter-spacing: .36px;
    padding: 0;
    line-height: 28px;
  }
  .course .cate-list .this{
    color: #ffc210;
    border: 1px solid #ffc210!important;
    border-radius: 30px;
  }
  .course .ordering::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .ordering ul{
    float: left;
  }
  .course .ordering ul::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .ordering .condition-result{
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    line-height: 28px;
  }
  .course .ordering ul li{
    float: left;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
  }
  .course .ordering .title{
    font-size: 16px;
    color: #888;
    letter-spacing: .36px;
    margin-left: 0;
    padding:0;
    line-height: 28px;
  }
  .course .ordering .this{
    color: #ffc210;
  }
  .course .ordering .price{
    position: relative;
  }
  .course .ordering .this::before,
  .course .ordering .this::after{
    cursor: pointer;
    content:"";
    display: block;
    width: 0px;
    height: 0px;
    border: 5px solid transparent;
    position: absolute;
    right: 0;
  }
  .course .ordering .this::before{
    border-bottom: 5px solid #aaa;
    margin-bottom: 2px;
    top: 2px;
  }
  .course .ordering .this::after{
    border-top: 5px solid #aaa;
    bottom: 2px;
  }
  .course .ordering .desc::after{
    border-top: 5px solid #ffc210;
  }
  .course .ordering .asc::before{
    border-bottom: 5px solid #ffc210;
  }
  .course .course-item:hover{
    box-shadow: 4px 6px 16px rgba(0,0,0,.5);
  }
  .course .course-item{
    width: 1050px;
    background: #fff;
    padding: 20px 30px 20px 20px;
    margin-bottom: 35px;
    border-radius: 2px;
    cursor: pointer;
    box-shadow: 2px 3px 16px rgba(0,0,0,.1);
    /* css3.0 过渡动画 hover 事件操作 */
    transition: all .2s ease;
  }
  .course .course-item::after{
    content:"";
    display: block;
    clear: both;
  }
  /* 顶级元素 父级元素  当前元素{} */
  .course .course-item .course-image{
    float: left;
    width: 423px;
    height: 210px;
    margin-right: 30px;
  }
  .course .course-item .course-image img{
    width: 100%;
  }
  .course .course-item .course-info{
    float: left;
    width: 596px;
  }
  .course-item .course-info h3 {
    font-size: 26px;
    color: #333;
    font-weight: normal;
    margin-bottom: 8px;
  }
  .course-item .course-info h3 span{
    font-size: 14px;
    color: #9b9b9b;
    float: right;
    margin-top: 14px;
  }
  .course-item .course-info h3 span img{
      width: 11px;
      height: auto;
      margin-right: 7px;
  }
  .course-item .course-info .teather-info{
      font-size: 14px;
      color: #9b9b9b;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid #333;
      border-bottom-color: rgba(51,51,51,.05);
  }
  .course-item .course-info .teather-info span{
      float: right;
  }
  .course-item .lesson-list::after{
      content:"";
      display: block;
      clear: both;
  }
  .course-item .lesson-list li {
    float: left;
    width: 44%;
    font-size: 14px;
    color: #666;
    padding-left: 22px;
    /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
    background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
    margin-bottom: 15px;
  }
  .course-item .lesson-list li .lesson-title{
      /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
      display:inline-block;
      max-width: 200px;
  }
  .course-item .lesson-list li:hover{
      background-image: url("/static/image/play-icon-yellow.svg");
      color: #ffc210;
  }
  .course-item .lesson-list li .free{
      width: 34px;
      height: 20px;
      color: #fd7b4d;
      vertical-align: super;
      margin-left: 10px;
      border: 1px solid #fd7b4d;
      border-radius: 2px;
      text-align: center;
      font-size: 13px;
      white-space: nowrap;
  }
  .course-item .lesson-list li:hover .free{
      color: #ffc210;
      border-color: #ffc210;
  }
  .course-item .pay-box::after{
    content:"";
    display: block;
    clear: both;
  }
  .course-item .pay-box .discount-type{
    padding: 6px 10px;
    font-size: 16px;
    color: #fff;
    text-align: center;
    margin-right: 8px;
    background: #fa6240;
    border: 1px solid #fa6240;
    border-radius: 10px 0 10px 0;
    float: left;
  }
  .course-item .pay-box .discount-price{
    font-size: 24px;
    color: #fa6240;
    float: left;
  }
  .course-item .pay-box .original-price{
    text-decoration: line-through;
    font-size: 14px;
    color: #9b9b9b;
    margin-left: 10px;
    float: left;
    margin-top: 10px;
  }
  .course-item .pay-box .buy-now{
    width: 120px;
    height: 38px;
    background: transparent;
    color: #fa6240;
    font-size: 16px;
    border: 1px solid #fd7b4d;
    border-radius: 3px;
    transition: all .2s ease-in-out;
    float: right;
    text-align: center;
    line-height: 38px;
  }
  .course-item .pay-boxthis .buy-now:hover{
    color: #fff;
    background: #ffc210;
    border: 1px solid #ffc210;
  }
  .el-pagination{
    text-align: center;
    margin-top: 18px;
    margin-bottom: 28px;
  }
</style>

import Vue from 'vue'
import Router from 'vue-router'
import Home from "@/components/Home"
import Login from "@/components/Login"
import Register from "@/components/Register"
import Course from "@/components/Course"
import Detail from "@/components/Detail"
import Cart from "@/components/Cart"
import Order from "@/components/Order"
import Success from "@/components/Success"
import User from "../components/User"
import UserOrder from "../components/UserOrder"
import Player from "../components/Player"
Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/',
      name: "Home",
      component: Home,
    },
    {
      name:"Home",
      path: "/home",
      component:Home,
    },
    {
      name:"Login",
      path: "/login",
      component: Login,
    },
    {
      name:"Register",
      path: "/register",
      component: Register,
    },
    {
      name:"Course",
      path: "/courses",
      component: Course,
    },
    {
      name:"Detail",
      path: "/courses/:id", // 在路由的路径中传递参数 /courses/4     // 查询字符串 courses/detail?id=4
      component: Detail,
    },
    {
      name:"Cart",
      path: "/cart",
      component: Cart,
    },
    {
      name:"Order",
      path: "/buy",
      component: Order,
    },
    {
      path: '/payments/result',
      name: "Success",
      component: Success,
    },
    {
      name:"User",
      path:"/my",
      component: User,
      // children:[  // 设置子路由,在父级路由对应的组件中如果存在父子公用部分页面,可以使用router-view来实现子路由
      //   {
      //     name:"UserOrder",
      //     path:"/order",
      //     component: UserOrder,
      //   }
      // ]
    },
    {
      name:"UserOrder",
      path:"/my/order",
      component: UserOrder,
    },
    {
      path: '/player',
      name: "Player",
      component: Player,
    },
  ]
})

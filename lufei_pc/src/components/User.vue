<template>
  <div>
  <Header/>
    个人中心
  <Footer/>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default{
    name:"User",
    data(){
      return {
      };
    },
    components:{
      Header,
      Footer,
    }
  }
</script>

<style scoped>

</style>

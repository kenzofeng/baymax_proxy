<template>
    <div>
    <navbar></navbar>
    <router-view></router-view>
    </div>
</template>

<script>
import navbar from './navbar/navbar'

export default {
  name: 'layout',
  components: {navbar}
}
</script>

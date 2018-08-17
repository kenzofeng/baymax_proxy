<template>
    <div>
        <div class="ui large divided aligned selection list">
            <item v-for="item in items" :key="item.pk" :item="item"> </item>
        </div>
    </div>
</template>

<script>
import item from './item'

export default {
  name: 'list',
  components: {item},
  props: {
    items: {}
  }
}
</script>
